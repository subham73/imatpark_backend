"""
Test for track exercise APIs
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
    TrackExercise,
    MuscleGroup,

)


from exercise.serializers import (
   TrackExerciseSerializer,
)

TRACK_EXERCISE_URL = reverse('exercise:track-exercise-list')
STRENGTH_EXERCISE_URL = reverse('exercise:strength-exercise-list')


def detail_url(exercise_id):
    """ Return track exercise detail URL"""
    return reverse('exercise:track-exercise-detail', args=[exercise_id])


def create_track_exercise(**params):
    """Create and return a sample track exercise"""
    defaults = {
        'name': 'jog',
    }
    defaults.update(params)

    track_exercise = TrackExercise.objects.create(**defaults)
    return track_exercise


def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


class PublicTrackExerciseApiTests(TestCase):
    """ Test unauthenticated exercise API access"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test that authentication is required"""
        res = self.client.get(reverse('exercise:track-exercise-list'))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTrackExerciseApiTests(TestCase):
    """ Test authenticated track_exercise API access"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_exercise(self):
        """ Test retrieving a list of exercises"""
        create_track_exercise()
        create_track_exercise(name='run')

        # get list of exercises from the url
        res = self.client.get(TRACK_EXERCISE_URL)

        # get all the exercises from the database
        track_exercise = TrackExercise.objects.all().order_by('-id')
        serializer = TrackExerciseSerializer(track_exercise, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # match the data from the database with the data from the url
        self.assertEqual(res.data, serializer.data)

    def test_track_exercise_is_avaialble_to_all_user(self):
        """Test that track_exercise is available to all user"""
        # logined in as user and created an track exercise
        track_exercise = create_track_exercise(name='run')

        other_user = create_user(
            email='other@example.com',
            password='test123',
        )
        # logined in as other user
        self.client.force_authenticate(other_user)

        res = self.client.get(TRACK_EXERCISE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # match data from url logined as other user has the
        # exercise created by user
        self.assertTrue(any(ex['id'] == track_exercise.id
                            for ex in res.data))

    def test_create_track_exercise(self):
        """Test creating a new track exercise"""
        # before we are creating the exercises in the database and
        # checking the get response is same or not
        payload = {
            'name': 'run',
        }
        res = self.client.post(TRACK_EXERCISE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # check if the exercise is created in the database
        track_exercise = TrackExercise.objects.get(id=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(track_exercise, key))

    def test_full_update_track_exercise(self):
        """Test full update of exercise"""
        track_exercise = create_track_exercise(
            name='jog',
        )

        payload = {
            'name': 'run',
        }

        url = detail_url(track_exercise.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        track_exercise.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(track_exercise, key))

    def test_delete_track_exercise(self):
        """Test delete exercise"""
        exercise = create_track_exercise()

        url = detail_url(exercise.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TrackExercise.objects.
                         filter(id=exercise.id).exists())

#     ##########################################################################
#     # muscle group tests
    def test_create_track_exercise_with_muscle_group_two_feild(self):
        """Test creating track exercise with primary and secondary
        muscle_groups"""
        payload = {
            'name': 'run',
            'primary_muscle_groups': [
                {'name': 'calves'},
            ],
            'secondary_muscle_groups': [
               {'name': 'arms'},
               {'name': 'quads'}
            ],
        }
        res = self.client.post(TRACK_EXERCISE_URL, payload, format='json')
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        track_exercises = TrackExercise.objects.all()
        self.assertEqual(track_exercises.count(), 1)
        track_exercise = track_exercises[0]
        self.assertEqual(track_exercise.primary_muscle_groups.count(), 1)
        self.assertEqual(track_exercise.secondary_muscle_groups.count(), 2)
        for primary_muscle_group in payload['primary_muscle_groups']:
            exists = track_exercise.primary_muscle_groups.filter(
                name=primary_muscle_group['name'],
            ).exists()
            self.assertTrue(exists)
        for secondary_muscle_group in payload['secondary_muscle_groups']:
            exists = track_exercise.secondary_muscle_groups.filter(
                name=secondary_muscle_group['name'],
            ).exists()
            self.assertTrue(exists)

    def test_create_exercise_with_existing_muscle_groups_two_feild(self):
        """Test creating a track_exercise with existing muscle_groups"""
        muscle_group_calves = MuscleGroup.objects.create(name='calves')
        muscle_group_arms = MuscleGroup.objects.create(name='arms')
        payload = {
            'name': 'run',
            'primary_muscle_groups': [
                {'name': 'calves'},
            ],
            'secondary_muscle_groups': [
               {'name': 'arms'},
            ],
        }
        res = self.client.post(TRACK_EXERCISE_URL, payload, format='json')
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        track_exercises = TrackExercise.objects.all()
        self.assertEqual(track_exercises.count(), 1)
        track_exercise = track_exercises[0]
        self.assertEqual(track_exercise.primary_muscle_groups.count(), 1)
        self.assertEqual(track_exercise.secondary_muscle_groups.count(), 1)
        self.assertIn(muscle_group_calves,
                      track_exercise.primary_muscle_groups.all())
        self.assertIn(muscle_group_arms,
                      track_exercise.secondary_muscle_groups.all())
        for muscle_group in payload['primary_muscle_groups']:
            exists = track_exercise.primary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)
        for muscle_group in payload['secondary_muscle_groups']:
            exists = track_exercise.secondary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)

    def test_create_muscle_group_on_update_two_feild(self):
        """Test creating muscle_group when updating a track exercise"""
        track_exercise = create_track_exercise()

        payload = {'primary_muscle_groups': [{'name': 'legs'}],
                   'secondary_muscle_groups': [{'name': 'arms'}],
                   }
        url = detail_url(track_exercise.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # track_exercise.refresh_from_db()
        new_muscle_group1 = MuscleGroup.objects.get(name='legs')
        self.assertIn(new_muscle_group1,
                      track_exercise.primary_muscle_groups.all())
        new_muscle_group2 = MuscleGroup.objects.get(name='arms')
        self.assertIn(new_muscle_group2,
                      track_exercise.secondary_muscle_groups.all())

    def test_primary_secondary_cant_have_same_muscle_group(self):
        """Test primary and secondary muscle_groups can't be same"""
        track_exercise = create_track_exercise()

        payload = {'primary_muscle_groups': [{'name': 'legs'}],
                   'secondary_muscle_groups': [{'name': 'legs'}],
                   }
        url = detail_url(track_exercise.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

##############################################################################
# test any conflit between muscle groups when present in track and strength
    def test_create_track_existing_strength_muscleGs(self):
        """Test creating track exercise with existing strength exercise
        muscle groups"""
        payload_Strength = {
            'name': 'strength exercise name',
            'description': 'Sample strength exercise description',
            'dificulty_level': 1,
            'primary_muscle_groups': [
                {'name': 'calves'},
            ],
            'secondary_muscle_groups': [
                {'name': 'arms'},
            ]
        }
        # checks if the strength exercise is created
        res = self.client.post(STRENGTH_EXERCISE_URL,
                               payload_Strength,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        strength_exercises = StrengthExercise.objects.all()
        self.assertEqual(strength_exercises.count(), 1)
        strength_exercise = strength_exercises[0]
        self.assertEqual(strength_exercise.primary_muscle_groups.count(), 1)
        self.assertEqual(strength_exercise.secondary_muscle_groups.count(), 1)
        # checks if the muscle groups are created
        for muscle_group in payload_Strength['primary_muscle_groups']:
            exists = strength_exercise.primary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)
        for muscle_group in payload_Strength['secondary_muscle_groups']:
            exists = strength_exercise.secondary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)

        payload_Track = {
            'name': 'run',
            'primary_muscle_groups': [
                {'name': 'arms'},
            ],
            'secondary_muscle_groups': [
               {'name': 'calves'},
            ],
        }
        # checks if the track exercise is created
        res = self.client.post(TRACK_EXERCISE_URL,
                               payload_Track,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        track_exercises = TrackExercise.objects.all()
        self.assertEqual(track_exercises.count(), 1)
        track_exercise = track_exercises[0]
        self.assertEqual(track_exercise.primary_muscle_groups.count(), 1)
        self.assertEqual(track_exercise.secondary_muscle_groups.count(), 1)
        # checks if the muscle groups are created
        for muscle_group in payload_Track['primary_muscle_groups']:
            exists = track_exercise.primary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)
        for muscle_group in payload_Track['secondary_muscle_groups']:
            exists = track_exercise.secondary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)

        # checks if the 2 muscle groups are prsent in the database
        muscle_group_arms = MuscleGroup.objects.all()
        self.assertEqual(muscle_group_arms.count(), 2)

    def test_update_trackEx_existing_strengthEx_muscleGs(self):
        """Test updating track exercise with existing strength exercise
        muscle groups"""
        track_exercise = create_track_exercise()

        # creating a strength exercising
        payload_Strength = {
            'name': 'strength exercise name',
            'description': 'Sample strength exercise description',
            'dificulty_level': 1,
            'primary_muscle_groups': [
                {'name': 'calves'},
            ],
            'secondary_muscle_groups': [
                {'name': 'arms'},
            ]
        }
        # checks if the strength exercise is created
        res = self.client.post(STRENGTH_EXERCISE_URL,
                               payload_Strength,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # updating the track exercise
        payload_Track = {'primary_muscle_groups': [{'name': 'calves'}],
                         'secondary_muscle_groups': [{'name': 'arms'}],
                         }
        url = detail_url(track_exercise.id)
        res = self.client.patch(url, payload_Track, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # track_exercise.refresh_from_db()
        track_exercises = TrackExercise.objects.all()
        self.assertEqual(track_exercises.count(), 1)
        track_exercise = track_exercises[0]
        self.assertEqual(track_exercise.primary_muscle_groups.count(), 1)
        self.assertEqual(track_exercise.secondary_muscle_groups.count(), 1)
        # checks if the muscle groups are created
        for muscle_group in payload_Track['primary_muscle_groups']:
            exists = track_exercise.primary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)
        for muscle_group in payload_Track['secondary_muscle_groups']:
            exists = track_exercise.secondary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)
