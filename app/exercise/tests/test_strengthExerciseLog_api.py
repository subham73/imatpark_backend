"""
Test for the Strength exercise Log API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    StrengthExercise,
    StrengthExerciseLog,
    TrackExerciseLog,
)

from exercise.serializers import (
    StrengthExerciseLogSerializer,
    # TrackExerciseLogSerializer,
)

STRENGTH_EXERCISE_LOG_URL = reverse('exercise:strength-exercise-log-list')
# TRACK_EXERCISE_LOG_URL = reverse('exercise:track-exercise-log-list')

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

class PublicStregthExerciseLogApiTests(TestCase):
    """"Test unautheticated exercise Log Api access"""
    def setup(self):
        self.client = APIClient()

    def test_authquired(self):
        """Test that authentication is required"""
        res = self.client.get(STRENGTH_EXERCISE_LOG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateStrengthExerciseLogApiTests(TestCase):
    """Test authenticated exercise Log API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_create_strength_exercise_log(self):
        """Test creating a strength exercise log and retrieving it via API"""
        # Create an exercise
        exercise = StrengthExercise.objects.create(name='Squats')

        # Data for creating a StrengthExerciseLog
        data = {
            'exercise': 'Squats',
            'reps': 10,
            'sets': 3,
            'calories_burned': 50
        }

        # Create the log via API
        response = self.client.post(STRENGTH_EXERCISE_LOG_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve the log via API
        response = self.client.get(STRENGTH_EXERCISE_LOG_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the serialized output
        logs = StrengthExerciseLog.objects.all()
        serializer = StrengthExerciseLogSerializer(logs, many=True)
        self.assertEqual(response.data, serializer.data)

        # Clean up
        exercise.delete()

    def test_create_strength_exercise_log_invalid_exercise(self):
        """Test creating a strength exercise log with an invalid exercise"""
        # Data with an invalid exercise name
        data = {
            'exercise': 'Nonexistent Exercise',
            'reps': 10,
            'sets': 3,
            'calories_burned': 50
        }

        # Attempt to create the log via API
        response = self.client.post(STRENGTH_EXERCISE_LOG_URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('exercise', response.data)