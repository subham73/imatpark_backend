"""
Test for exercise APIs
"""
# from decimal import Decimal
# import os
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Exercise,
)

from exercise.serializers import (
    ExerciseSerializer,
    ExerciseDetailSerializer,
)

EXERCISE_URL = reverse('exercise:exercise-list')


def detail_url(exercise_id):
    """ Return exercise detail URL"""
    return reverse('exercise:exercise-detail', args=[exercise_id])


def create_exercise(**params):
    """Create and return a sample exercise"""
    defaults = {
        'name': 'shoulder push-up',
        'description': 'Sample Exercise Description',
        'dificulty_level': 3
    }
    defaults.update(params)

    exercise = Exercise.objects.create(**defaults)
    return exercise


def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


class PublicExerciseApiTests(TestCase):
    """ Test unauthenticated exercise API access"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test that authentication is required"""
        res = self.client.get(reverse('exercise:exercise-list'))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateExerciseApiTests(TestCase):
    """ Test authenticated exercise API access"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_exercise(self):
        """ Test retrieving a list of exercises"""
        create_exercise()
        create_exercise(name='Pull-up', dificulty_level=2)

        # get list of exercises from the url
        res = self.client.get(EXERCISE_URL)

        # get all the exercises from the database
        exercises = Exercise.objects.all().order_by('-id')
        serializer = ExerciseSerializer(exercises, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # match the data from the database with the data from the url
        self.assertEqual(res.data, serializer.data)

    def test_exercise_is_avaialble_to_all_user(self):
        """Test that exercise is available to all user"""
        # logined in as user and created an exercise
        exercise = create_exercise(name='jump-up', dificulty_level=2)

        other_user = create_user(
            email='other@example.com',
            password='test123',
        )
        # logined in as other user
        self.client.force_authenticate(other_user)

        res = self.client.get(EXERCISE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # match data from url logined as other user has the
        # exercise created by user
        self.assertTrue(any(ex['id'] == exercise.id for ex in res.data))

    def test_get_exercise_detail(self):
        """Test get exercise detail"""
        exercise = create_exercise()

        url = detail_url(exercise.id)
        res = self.client.get(url)

        serializer = ExerciseDetailSerializer(exercise)
        self.assertEqual(res.data, serializer.data)

    def test_description_not_availble_in_Exercise_Serializer(self):
        """Test description is only availble by detailSerializer"""
        payload = {
            'name': 'jump-up',
            'description': 'Sample Exercise Description',
            'dificulty_level': 2
        }
        exercise = create_exercise(**payload)

        res_normal_url = self.client.get(EXERCISE_URL)
        url_details = detail_url(exercise.id)
        res_detail_url = self.client.get(url_details)

        self.assertEqual(res_normal_url.status_code, status.HTTP_200_OK)
        self.assertEqual(res_detail_url.status_code, status.HTTP_200_OK)
        # check if description is not in the normal url
        self.assertNotIn('description', res_normal_url.data[0])
        # check if description is in the detail url
        self.assertIn('description', res_detail_url.data)
        self.assertEqual(res_detail_url.data['description'],
                         payload['description'])

    def test_create_exercise(self):
        """Test creating a new exercise"""
        # before we are creating the exercises in the database and
        # checking the get response is same or not
        payload = {
            'name': 'new exercise name',
            'description': 'Sample Exercise Description',
            'dificulty_level': 3
        }
        res = self.client.post(EXERCISE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # check if the exercise is created in the database
        exercise = Exercise.objects.get(id=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(exercise, key))

    def test_partial_update_exercise(self):
        """Test partial update of exercise"""
        # created an exercise in the database
        exercise = create_exercise(
            name='Sample exercise name',
            description="Sample exercise description",
            dificulty_level=1,
        )

        payload = {'name': 'New exercise name'}
        url = detail_url(exercise.id)
        # updating the exercise
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        exercise.refresh_from_db()
        self.assertEqual(exercise.name, payload['name'])

    def test_full_update_exercise(self):
        """Test full update of exercise"""
        exercise = create_exercise(
            name='Sample exercise name',
            description="Sample exercise description",
            dificulty_level=1,
        )

        payload = {
            'name': 'new exercise name',
            'description': 'new exercise description',
            'dificulty_level': 2,
        }

        url = detail_url(exercise.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        exercise.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(exercise, key))

    def test_delete_exercise(self):
        """Test delete exercise"""
        exercise = create_exercise()

        url = detail_url(exercise.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Exercise.objects.filter(id=exercise.id).exists())
