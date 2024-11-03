from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import StrengthExercise, StrengthExerciseLog
from ..analytics.services import get_user_log_analytics

ANALYTICS_URL = reverse('user:analytics')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_strength_exercise(**params):
    """Create and return a sample strength exercise"""
    defaults = {
        'name': 'arms push-up',
        'description': 'Sample StrengthExercise Description',
        'dificulty_level': 3
    }
    defaults.update(params)


class UserAnalyticsApiTests(TestCase):
    """Test the user analytics API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_analytics(self):
        """Test retrieving user analytics"""
        # Create some exercise logs for the user
        exercise1 = StrengthExercise.objects.create(name='jump')
        exercise2 = StrengthExercise.objects.create(name='pull-up')
        StrengthExerciseLog.objects.create(
            user=self.user,
            exercise=exercise1,
            reps=10,
            sets=3,
            calories_burned=50
        )
        StrengthExerciseLog.objects.create(
            user=self.user,
            exercise=exercise2,
            reps=15,
            sets=4,
            calories_burned=70
        )

        # Make the API request
        res = self.client.get(ANALYTICS_URL)

        # Check the response
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Calculate expected analytics
        expected_analytics = get_user_log_analytics(self.user)

        # Verify the response data
        self.assertEqual(res.data, expected_analytics)
