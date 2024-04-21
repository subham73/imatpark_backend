"""
Tests for the muscle_groups API endpoint
"""
# from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import MuscleGroup, StrengthExercise
from exercise.serializers import MuscleGroupSerializer

MUSCLE_GROUP_URL = reverse('exercise:muscle-group-list')

def detail_url(muscle_group_id):
    """Return muscle_group detail URL"""
    return reverse('exercise:muscle-group-detail', args=[muscle_group_id])

def create_user(email="user@example.com", password="testpass123"):
    """Create and return a user"""
    return get_user_model().objects.create_user(email=email, password=password)

def PublicMusleGroupsApiTests(TestCase):
    """Test unauthenticated API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving muscle groups"""
        res = self.client.get(MUSCLE_GROUP_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateMusleGroupsApiTests(TestCase):
    """Test the authenticated API requests"""
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # def test_underthehood_when_object_is_created_with_less_field(self):
    #     """Test creating muscle_group with less fields"""
    #     MuscleGroup.objects.create(name='legs')
    #     res = self.client.get(MUSCLE_GROUP_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, {'id': 1, 'name': 'legs', 'description': ''})

    def test_retrieve_muscle_group(self):
        """Test retrieving Muscle Group"""
        MuscleGroup.objects.create(name='legs')
        MuscleGroup.objects.create(name='calves')

        res = self.client.get(MUSCLE_GROUP_URL)

        muscle_groups = MuscleGroup.objects.all().order_by('-name')
        self.assertEqual(muscle_groups.count(), 2)
        serializer = MuscleGroupSerializer(muscle_groups, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_muscle_group(self):
        """Test updating a muscle_group"""
        muscle_group = MuscleGroup.objects.create(name='calves')
        payload = {'name': 'legs'}
        url = detail_url(muscle_group.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        muscle_group.refresh_from_db()
        self.assertEqual(muscle_group.name, payload['name'])

    def test_delete_muscle_group(self):
        """Test deleting a muscle_group"""
        muscle_group = MuscleGroup.objects.create(name='calves')
        url = detail_url(muscle_group.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MuscleGroup.objects.count(), 0)
        #or can be written as
        #muscle_groups = MuscleGroup.objects.filter(user=self.user)
        # self.assertFalse(muscle_groups.exists())

    # def test_filter_muscle_groups_assigned_to_strength_exercise(self):
    #     """Test filtering muscle_groups by those assigned to recipes"""
    #     muscle_group1 = MuscleGroup.objects.create(name='calves')
    #     muscle_group2 = MuscleGroup.objects.create(name='Abs')
    #     strength_exercise = StrengthExercise.objects.create(
    #         name='Push-up',
    #         dificulty_level=1,
    #     )
    #     strength_exercise.primary_muscle_groups.add(muscle_group1)

    #     res = self.client.get(MUSCLE_GROUP_URL, {'assigned_only': 1})
    #     serializer1 = MuscleGroupSerializer(muscle_group1)
    #     serializer2 = MuscleGroupSerializer(muscle_group2)
    #     print(res.data)
    #     self.assertIn(serializer1.data, res.data)
    #     self.assertNotIn(serializer2.data, res.data)

    # def test_filtered_muscle_groups_assigned_unique(self):
    #     """Test filtering muscle_groups by assigned returns unique items"""
    #     muscle_group = MuscleGroup.objects.create(name='legs')
    #     MuscleGroup.objects.create(name='calves')
    #     strength_exercise1 = StrengthExercise.objects.create(
    #         name='Push-up',
    #         dificulty_level=1,
    #     )
    #     strength_exercise1.primary_muscle_groups.add(muscle_group)
    #     strength_exercise2 = StrengthExercise.objects.create(
    #         name='Pull-up',
    #         dificulty_level=2,
    #     )
    #     strength_exercise2.primary_muscle_groups.add(muscle_group)

    #     res = self.client.get(MUSCLE_GROUP_URL, {'assigned_only': 1})
    #     print(res.data)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], muscle_group.name)