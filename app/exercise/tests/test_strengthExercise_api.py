"""
Test for strength exercise APIs
"""
# from decimal import Decimal
import tempfile
import os

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    StrengthExercise,
    MuscleGroup,
    TrackExercise
)

from exercise.serializers import (
    StrengthExerciseSerializer,
    StrengthExerciseDetailSerializer,
)

STRENGTH_EXERCISE_URL = reverse('exercise:strength-exercise-list')
TRACK_EXERCISE_URL = reverse('exercise:track-exercise-list')


def detail_url(exercise_id):
    """ Return strength exercise detail URL"""
    return reverse('exercise:strength-exercise-detail', args=[exercise_id])


def image_upload_url(exercise_id):
    """Return URL for strength exercise image upload"""
    return reverse('exercise:strength-exercise-upload-image',
                   args=[exercise_id])


def create_strength_exercise(**params):
    """Create and return a sample strength exercise"""
    defaults = {
        'name': 'arms push-up',
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

    ##########################################################################
    # primary muscle group tests

    def test_create_strength_exercise_with_muscle_group(self):
        """Test creating strength_exercise with new muscle_groups"""
        payload = {
            'name': 'Sample strength exercise name',
            'description': 'Sample strength exercise description',
            'dificulty_level': 1,
            'primary_muscle_groups': [
                {'name': 'calves'},
                {'name': 'arms'},
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
        """Test creating a strength_exercise with existing muscle_groups"""
        muscle_group_calves = MuscleGroup.objects.create(name='calves')
        payload = {
            'name': 'strength exercise name',
            'description': 'Sample strength exercise description',
            'dificulty_level': 1,
            'primary_muscle_groups': [
                {'name': 'calves'},
                {'name': 'arms'},
            ]
        }
        res = self.client.post(STRENGTH_EXERCISE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        strength_exercises = StrengthExercise.objects.all()
        self.assertEqual(strength_exercises.count(), 1)
        strength_exercise = strength_exercises[0]
        self.assertEqual(strength_exercise.primary_muscle_groups.count(), 2)
        self.assertIn(muscle_group_calves,
                      strength_exercise.primary_muscle_groups.all())
        for muscle_group in payload['primary_muscle_groups']:
            exists = strength_exercise.primary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)

    def test_create_muscle_group_on_update(self):
        """Test creating muscle_group when updating a strength_exercise"""
        strength_exercise = create_strength_exercise()

        payload = {'primary_muscle_groups': [{'name': 'legs'}]}
        url = detail_url(strength_exercise.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # strength_exercise.refresh_from_db()
        new_muscle_group = MuscleGroup.objects.get(name='legs')
        self.assertIn(new_muscle_group,
                      strength_exercise.primary_muscle_groups.all())

    def test_update_strength_exercise_assign_muscle_group(self):
        """Test assigning an existing muscle_group when updating a
        strength_exercise"""
        muscle_group_core = MuscleGroup.objects.create(name='core',)
        strength_exercise = create_strength_exercise()
        strength_exercise.primary_muscle_groups.add(muscle_group_core)

        muscle_group_abs = MuscleGroup.objects.create(name='abs')
        payload = {'primary_muscle_groups': [{'name': 'abs'}]}
        url = detail_url(strength_exercise.id)
        res = self.client.patch(url, payload, format='json')

        # dono add ho gaye hai
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(muscle_group_abs,
                      strength_exercise.primary_muscle_groups.all())
        self.assertNotIn(muscle_group_core,
                         strength_exercise.primary_muscle_groups.all())

    def test_clear_strength_exercise_muscle_groups(self):
        """Test clearing all muscle_groups of a strength_exercise"""
        muscle_group_abs = MuscleGroup.objects.create(name='abs')
        strength_exercise = create_strength_exercise()
        strength_exercise.primary_muscle_groups.add(muscle_group_abs)

        payload = {'primary_muscle_groups': []}
        url = detail_url(strength_exercise.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(strength_exercise.primary_muscle_groups.count(), 0)

    ##########################################################################
    # secondary muscle group test

    def test_create_strength_exercise_with_muscle_group_two_feild(self):
        """Test creating strength exercise with primary and secondary
        muscle_groups"""
        payload = {
            'name': 'Sample strength exercise name',
            'description': 'Sample strength exercise description',
            'dificulty_level': 1,
            'primary_muscle_groups': [
                {'name': 'calves'},
            ],
            'secondary_muscle_groups': [
               {'name': 'arms'},
               {'name': 'quads'}
            ],
        }
        res = self.client.post(STRENGTH_EXERCISE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        strength_exercises = StrengthExercise.objects.all()
        self.assertEqual(strength_exercises.count(), 1)
        strength_exercise = strength_exercises[0]
        self.assertEqual(strength_exercise.primary_muscle_groups.count(), 1)
        self.assertEqual(strength_exercise.secondary_muscle_groups.count(), 2)
        for primary_muscle_group in payload['primary_muscle_groups']:
            exists = strength_exercise.primary_muscle_groups.filter(
                name=primary_muscle_group['name'],
            ).exists()
            self.assertTrue(exists)
        for secondary_muscle_group in payload['secondary_muscle_groups']:
            exists = strength_exercise.secondary_muscle_groups.filter(
                name=secondary_muscle_group['name'],
            ).exists()
            self.assertTrue(exists)

    def test_create_exercise_with_existing_muscle_groups_two_feild(self):
        """Test creating a strength_exercise with existing muscle_groups"""
        muscle_group_calves = MuscleGroup.objects.create(name='calves')
        muscle_group_arms = MuscleGroup.objects.create(name='arms')
        payload = {
            'name': 'strength exercise name',
            'description': 'Sample strength exercise description',
            'dificulty_level': 1,
            'primary_muscle_groups': [
                {'name': 'calves'},
            ],
            'secondary_muscle_groups': [
               {'name': 'arms'},
            ],
        }
        res = self.client.post(STRENGTH_EXERCISE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        strength_exercises = StrengthExercise.objects.all()
        self.assertEqual(strength_exercises.count(), 1)
        strength_exercise = strength_exercises[0]
        self.assertEqual(strength_exercise.primary_muscle_groups.count(), 1)
        self.assertEqual(strength_exercise.secondary_muscle_groups.count(), 1)
        self.assertIn(muscle_group_calves,
                      strength_exercise.primary_muscle_groups.all())
        self.assertIn(muscle_group_arms,
                      strength_exercise.secondary_muscle_groups.all())
        for muscle_group in payload['primary_muscle_groups']:
            exists = strength_exercise.primary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)
        for muscle_group in payload['secondary_muscle_groups']:
            exists = strength_exercise.secondary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)

    def test_create_muscle_group_on_update_two_feild(self):
        """Test creating muscle_group when updating a strength_exercise"""
        strength_exercise = create_strength_exercise()

        payload = {'primary_muscle_groups': [{'name': 'legs'}],
                   'secondary_muscle_groups': [{'name': 'arms'}],
                   }
        url = detail_url(strength_exercise.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # strength_exercise.refresh_from_db()
        new_muscle_group1 = MuscleGroup.objects.get(name='legs')
        self.assertIn(new_muscle_group1,
                      strength_exercise.primary_muscle_groups.all())
        new_muscle_group2 = MuscleGroup.objects.get(name='arms')
        self.assertIn(new_muscle_group2,
                      strength_exercise.secondary_muscle_groups.all())

    def test_primary_secondary_cant_have_same_muscle_group(self):
        """Test primary and secondary muscle_groups can't be same"""
        strength_exercise = create_strength_exercise()

        payload = {'primary_muscle_groups': [{'name': 'legs'}],
                   'secondary_muscle_groups': [{'name': 'legs'}],
                   }
        url = detail_url(strength_exercise.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

##############################################################################
# test any conflit between muscle groups when present in  strength and track
    def test_create_strengthEx_existing_trackEx_muscleGs(self):
        """Test creating strength exercise with existing track exercise
        muscle groups"""
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

        # checks if the 2 muscle groups are prsent in the database
        muscle_group_arms = MuscleGroup.objects.all()
        self.assertEqual(muscle_group_arms.count(), 2)

    def test_update_strengthEx_existing_trackEx_muscleGs(self):
        """Test updating track exercise with existing strength exercise
        muscle groups"""
        strength_exercise = create_strength_exercise()

        # creating a track exercising
        payload_Track = {
            'name': 'run',
            'primary_muscle_groups': [
                {'name': 'calves'},
            ],
            'secondary_muscle_groups': [
                {'name': 'arms'},
            ]
        }
        # checks if the strength exercise is created
        res = self.client.post(TRACK_EXERCISE_URL,
                               payload_Track,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # updating the track exercise
        payload_Exercise = {'primary_muscle_groups': [{'name': 'calves'}],
                            'secondary_muscle_groups': [{'name': 'arms'}],
                            }
        url = detail_url(strength_exercise.id)
        res = self.client.patch(url, payload_Exercise, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # track_exercise.refresh_from_db()
        strength_exercises = StrengthExercise.objects.all()
        self.assertEqual(strength_exercises.count(), 1)
        strength_exercise = strength_exercises[0]
        self.assertEqual(strength_exercise.primary_muscle_groups.count(), 1)
        self.assertEqual(strength_exercise.secondary_muscle_groups.count(), 1)
        # checks if the muscle groups are created
        for muscle_group in payload_Track['primary_muscle_groups']:
            exists = strength_exercise.primary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)
        for muscle_group in payload_Track['secondary_muscle_groups']:
            exists = strength_exercise.secondary_muscle_groups.filter(
                name=muscle_group['name'],
            ).exists()
            self.assertTrue(exists)

##############################################################################


class ImageUploadTests(TestCase):
    """Test image upload for strength exercise"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)
        self.exercise = create_strength_exercise()

    def tearDown(self):
        self.exercise.image.delete()

    def test_upload_image_to_strength_exercise(self):
        """Test uploading an image to strength exercise"""
        url = image_upload_url(self.exercise.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)  # move the pointer to the start of the file
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.exercise.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.exercise.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.exercise.id)
        payload = {'image': 'noRandomImage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
