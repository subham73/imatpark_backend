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
    StrengthExercise,
    MuscleGroup,
)

from exercise.serializers import (
    StrengthExerciseSerializer,
    StrengthExerciseDetailSerializer,
)

STRENGTH_EXERCISE_URL = reverse('exercise:strength-exercise-list')


def detail_url(exercise_id):
    """ Return strength exercise detail URL"""
    return reverse('exercise:strength-exercise-detail', args=[exercise_id])


def create_strength_exercise(**params):
    """Create and return a sample strength exercise"""
    defaults = {
        'name': 'shoulder push-up',
        'description': 'Sample StrengthExercise Description',
        'dificulty_level': 3
    }
    defaults.update(params)

    strength_exercise = StrengthExercise.objects.create(**defaults)
    return strength_exercise


def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


class PublicStrengthExerciseApiTests(TestCase):
    """ Test unauthenticated exercise API access"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test that authentication is required"""
        res = self.client.get(reverse('exercise:strength-exercise-list'))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStrengthExerciseApiTests(TestCase):
    """ Test authenticated strength_exercise API access"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_exercise(self):
        """ Test retrieving a list of exercises"""
        create_strength_exercise()
        create_strength_exercise(name='Pull-up', dificulty_level=2)

        # get list of exercises from the url
        res = self.client.get(STRENGTH_EXERCISE_URL)

        # get all the exercises from the database
        strength_exercise = StrengthExercise.objects.all().order_by('-id')
        serializer = StrengthExerciseSerializer(strength_exercise, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # match the data from the database with the data from the url
        self.assertEqual(res.data, serializer.data)

    def test_strength_exercise_is_avaialble_to_all_user(self):
        """Test that strength_exercise is available to all user"""
        # logined in as user and created an strength exercise
        strength_exercise = create_strength_exercise(name='jump-up',
                                                     dificulty_level=2)

        other_user = create_user(
            email='other@example.com',
            password='test123',
        )
        # logined in as other user
        self.client.force_authenticate(other_user)

        res = self.client.get(STRENGTH_EXERCISE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # match data from url logined as other user has the
        # exercise created by user
        self.assertTrue(any(ex['id'] == strength_exercise.id
                            for ex in res.data))

    def test_get_strength_exercise_detail(self):
        """Test get strength exercise detail"""
        strength_exercise = create_strength_exercise()

        url = detail_url(strength_exercise.id)
        res = self.client.get(url)

        serializer = StrengthExerciseDetailSerializer(strength_exercise)
        self.assertEqual(res.data, serializer.data)

    def test_description_not_availble_in_StrengthExercise_Serializer(self):
        """Test description is only availble by detailSerializer"""
        payload = {
            'name': 'jump-up',
            'description': 'Sample StrengthExercise Description',
            'dificulty_level': 2
        }
        strength_exercise = create_strength_exercise(**payload)

        res_normal_url = self.client.get(STRENGTH_EXERCISE_URL)
        url_details = detail_url(strength_exercise.id)
        res_detail_url = self.client.get(url_details)

        self.assertEqual(res_normal_url.status_code, status.HTTP_200_OK)
        self.assertEqual(res_detail_url.status_code, status.HTTP_200_OK)
        # check if description is not in the normal url
        self.assertNotIn('description', res_normal_url.data[0])
        # check if description is in the detail url
        self.assertIn('description', res_detail_url.data)
        self.assertEqual(res_detail_url.data['description'],
                         payload['description'])

    def test_create_strength_exercise(self):
        """Test creating a new strength exercise"""
        # before we are creating the exercises in the database and
        # checking the get response is same or not
        payload = {
            'name': 'new strength exercise name',
            'description': 'Sample StrengthExercise Description',
            'dificulty_level': 3
        }
        res = self.client.post(STRENGTH_EXERCISE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # check if the exercise is created in the database
        strength_exercise = StrengthExercise.objects.get(id=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(strength_exercise, key))

    def test_partial_update_strength_exercise(self):
        """Test partial update of strength exercise"""
        # created an exercise in the database
        strength_exercise = create_strength_exercise(
            name='Sample strength exercise name',
            description="Sample strength exercise description",
            dificulty_level=1,
        )

        payload = {'name': 'New strength exercise name'}
        url = detail_url(strength_exercise.id)
        # updating the exercise
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        strength_exercise.refresh_from_db()
        self.assertEqual(strength_exercise.name, payload['name'])

    def test_full_update_strength_exercise(self):
        """Test full update of exercise"""
        strength_exercise = create_strength_exercise(
            name='Sample strength exercise name',
            description="Sample strength exercise description",
            dificulty_level=1,
        )

        payload = {
            'name': 'new strength exercise name',
            'description': 'new strength exercise description',
            'dificulty_level': 2,
        }

        url = detail_url(strength_exercise.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        strength_exercise.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(strength_exercise, key))

    def test_delete_strength_exercise(self):
        """Test delete exercise"""
        exercise = create_strength_exercise()

        url = detail_url(exercise.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(StrengthExercise.objects.
                         filter(id=exercise.id).exists())

    def test_create_strength_exercise_with_muscle_group(self):
        """Test creating strength_exercise with new muscle_groups"""
        payload = {
            'name': 'Sample strength exercise name',
            'description': 'Sample strength exercise description',
            'dificulty_level': 1,
            'primary_muscle_groups': [
                {'name': 'chest', 'description': 'chest muscles'},
                {'name': 'shoulder', 'description': 'shoulder muscles'},
            ]
        }
        res = self.client.post(STRENGTH_EXERCISE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        strength_exercises = StrengthExercise.objects.all()
        self.assertEqual(strength_exercises.count(), 1)
        strength_exercise = strength_exercises[0]
        self.assertEqual(strength_exercise.primary_muscle_groups.count(), 2)
        for primary_muscle_group in payload['primary_muscle_groups']:
            exists = strength_exercise.primary_muscle_groups.filter(
                name=primary_muscle_group['name'],
            ).exists()
            self.assertTrue(exists)

    def test_create_strength_exercise_with_existing_muscle_groups(self):
        """Test creatring a strength_exercise with existing muscle_groups"""
        muscle_group_chest = MuscleGroup.objects.create(name='chest', description='chest muscles')
        payload={
            'name': 'strength exercise name',
            'description': 'Sample strength exercise description',
            'dificulty_level': 1,
            'primary_muscle_groups': [
                {'name': 'chest', 'description': 'chest muscles'},
                {'name': 'shoulder', 'description': 'shoulder muscles'},
            ]
        }
        res = self.client.post(STRENGTH_EXERCISE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        strength_exercises = StrengthExercise.objects.all()
        self.assertEqual(strength_exercises.count(), 1)
        strength_exercise = strength_exercises[0]
        self.assertEqual(strength_exercise.primary_muscle_groups.count(), 2)
        self.assertIn(muscle_group_chest, strength_exercise.primary_muscle_groups.all())
        for muscle_group in payload['primary_muscle_groups']:
            exists = strength_exercise.primary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)

    def test_create_muscle_group_on_update(self):
        """Test creating muscle_group when updating a strength_exercise"""
        strength_exercise = create_strength_exercise()

        payload = {'primary_muscle_groups':[{'name': 'leg', 'description': 'leg muscles'}]}
        url = detail_url(strength_exercise.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # strength_exercise.refresh_from_db()
        new_muscle_group = MuscleGroup.objects.get(name='leg')
        self.assertIn(new_muscle_group, strength_exercise.primary_muscle_groups.all())

    def test_update_strength_exercise_assign_muscle_group(self):
        """Test assigning an existing muscle_group when updating a strength_exercise"""
        muscle_group_core = MuscleGroup.objects.create(name='core')
        strength_exercise = create_strength_exercise()
        strength_exercise.primary_muscle_groups.add(muscle_group_core)

        muscle_group_abs = MuscleGroup.objects.create(name='Abs', description='Abs muscles')
        payload = {'primary_muscle_groups': [{'name': 'Abs', 'description': 'Abs muscles'}]}
        url = detail_url(strength_exercise.id)
        res = self.client.patch(url, payload, format='json') # bas lunch hai

        # dono add ho gaye hai
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(muscle_group_abs, strength_exercise.primary_muscle_groups.all())
        self.assertNotIn(muscle_group_core, strength_exercise.primary_muscle_groups.all())

    def test_clear_strength_exercise_muscle_groups(self):
        """Test clearing all muscle_groups of a strength_exercise"""
        muscle_group_core = MuscleGroup.objects.create(name='Core')
        strength_exercise = create_strength_exercise()
        strength_exercise.primary_muscle_groups.add(muscle_group_core)

        payload = {'primary_muscle_groups': []}
        url = detail_url(strength_exercise.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(strength_exercise.primary_muscle_groups.count(), 0)
