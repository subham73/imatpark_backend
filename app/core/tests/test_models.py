'''
Tests for models
'''
# from unittest.mock import patch
# from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from core import models

from datetime import datetime as dt
import datetime

current_year = dt.now().year


def create_user(email="user@example.com",
                password="testpass123",
                **extra_fields):
    """Create a sample user"""
    return get_user_model().objects.create_user(email,
                                                password,
                                                extra_fields)


class ModelTests(TestCase):
    """Test models."""
##############################################################################
# The following tests are for the User model
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.Com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email in sample_email:
            user = get_user_model().objects.create_user(email[0], 'test123')
            self.assertEqual(user.email, email[1])

    def test_new_user_without_email_raises_error(self):
        """ Test that creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_new_user_valid_height_weight(self):
        """Test the creation of user with valid
             height and weight """
        paylaod = {
            'height': 120,
            'weight': 80,
        }
        user = get_user_model().objects.create_user(
            'test@example.com',
            'test123',
            height=paylaod['height'],
            weight=paylaod['weight'],
        )
        self.assertEqual(user.height, paylaod['height'])
        self.assertEqual(user.weight, paylaod['weight'])

    def test_new_user_invalid_height_weight(self):
        """Test the invalid height and weight for a new user"""
        email = 'user@example.com'
        password = "pass@123"
        user = get_user_model().objects.create_user(
                email=email,
                password=password,
            )
        invalid_height_and_weight = [
            [0, 0],
            [-1, -2],
            [0, 100],
            [49, 19],  # Values just below the minimum allowed values
            [301, 1001]  # Values just above the maximum allowed values
        ]
        exceptions_count = 0
        for height, weight in invalid_height_and_weight:
            user.height = height
            user.weight = weight
            try:
                user.full_clean()
            except ValidationError:
                exceptions_count += 1
        self.assertEqual(exceptions_count, len(invalid_height_and_weight))

    def test_new_user_valid_year_of_birth(self):
        """Test the creation on a new user with valid year of birth"""
        payload = {
            'year_of_birth': 2001,
        }
        user = get_user_model().objects.create_user(
            'test@example.com',
            'test123',
            year_of_birth=payload['year_of_birth'],
        )
        self.assertEqual(user.year_of_birth, payload['year_of_birth'])

    def test_new_user_invalid_year_of_birth(self):
        """Test the year of birth for a new user"""
        email = 'user@example.com'
        password = "pass@123"
        user = get_user_model().objects.create_user(
                email=email,
                password=password,
            )
        invalid_years = [
            -12,   # Negative values
            0,     # Zero
            1899,  # Values just below the minimum allowed values
            current_year-1,  # Values just above the maximum allowed values
            current_year+2,  # Values in the future
        ]

        exceptions_count = 0
        for year in invalid_years:
            user.year_of_birth = year
            try:
                user.full_clean()
            except ValidationError:
                exceptions_count += 1
        self.assertEqual(exceptions_count, len(invalid_years))

##############################################################################
# The following tests are for the User Strength Exercise model

    def test_create_StrengthExercise(self):
        """Test the StrengthExercise string representation"""

        strength_exercise = models.StrengthExercise.objects.create(
            name='Pull-up',
            description='Pull-up exercise',
            dificulty_level=2
        )

        self.assertEqual(str(strength_exercise), strength_exercise.name)

    def test_create_MuscleGroup(self):
        """Test the MuscleGroup string representation"""

        muscle_group = models.MuscleGroup.objects.create(
            name='hamstrings',
        )

        self.assertEqual(str(muscle_group), muscle_group.name)

    def test_create_StrengthExercise_with_primary_muscle_group(self):
        """Test creating a StrengthExercise with muscle group"""

        muscle_group = models.MuscleGroup.objects.create(
            name='hamstrings',
        )

        strength_exercise = models.StrengthExercise.objects.create(
            name='Pull-up',
            description='Pull-up exercise',
            dificulty_level=2
        )

        strength_exercise.primary_muscle_groups.add(muscle_group)
        strength_exercise.secondary_muscle_groups.add(muscle_group)

        self.assertEqual(strength_exercise.primary_muscle_groups.count(), 1)
        self.assertEqual(strength_exercise.secondary_muscle_groups.count(), 1)

##############################################################################
# The following tests are for the Track exercise model
    def test_create_TrackExercise(self):
        """Test the TrackExercise string representation"""

        track_exercise = models.TrackExercise.objects.create(
            name='run',
        )

        self.assertEqual(str(track_exercise), track_exercise.name)

    def test_create_TrackExercise_with_pri_secondary_muscle_group(self):
        """Test creating a TrackExercise with muscle group"""

        muscle_group1 = models.MuscleGroup.objects.create(
            name='hamstrings',
        )
        muscle_group2 = models.MuscleGroup.objects.create(
            name='quads',
        )

        track_exercise = models.TrackExercise.objects.create(
            name='walk',
        )

        track_exercise.primary_muscle_groups.add(muscle_group1)
        track_exercise.secondary_muscle_groups.add(muscle_group2)

        self.assertEqual(track_exercise.primary_muscle_groups.count(), 1)
        self.assertEqual(track_exercise.secondary_muscle_groups.count(), 1)

##############################################################################
# The following tests are for the strength Exercise Log

    # def test_create_StrengthExerciseLog(self):
    #     user=get_user_model().objects.create_user(
    #             email='user@example.com',
    #             password='pass@123',
    #         )
    #     strength_exercise=models.StrengthExercise.objects.create(
    #             name='Pull-up',
    #             description='Pull-up exercise',
    #             dificulty_level=2
    #             )
    #     date = datetime.date.today()
    #     strength_exercise_log = models.StrengthExerciseLog.objects.create(
    #         user=user,
    #         exercise=strength_exercise,
    #         sets=3,
    #         reps=10,
    #         calories_burned=100,
    #     )

    #     expected_output = f'{user.email} - {strength_exercise.name} - {date}'
    #     self.assertEqual(str(strength_exercise_log), expected_output)





# class ExerciseLogTests(TestCase):
#     """Test the ExerciseLog model"""
#     def setUp(self):
#         email = 'user@example.com'
#         password = "pass@123"
#         self.user = get_user_model().objects.create_user(
#                 email=email,
#                 password=password,
#             )
#         self.strength_exercise = models.StrengthExercise.objects.create(
#             name='Pull-up',
#             description='Pull-up exercise',
#             # difficulty_level=2
#         )
#         self.date = datetime.date.today()

#     def test_create_StrengthExerciseLog(self):
#         strength_exercise_log = models.StrengthExerciseLog.objects.create(
#             user=self.user,
#             exercise=self.strength_exercise,
#             sets=3,
#             reps=10,
#             date=self.date,
#         )

#         expected_output = f'{self.user.email} - {self.strength_exercise.name} - {self.date}'
#         self.assertEqual(str(strength_exercise_log), expected_output)

        # def test_create_StrengthExerciseLog_with_invalid_sets_reps_weight(self):
        #     """Test creating a StrengthExerciseLog with invalid sets, reps and weight"""

        #     user = create_user()
        #     strength_exercise = models.StrengthExercise.objects.create(
        #         name='Pull-up',
        #         description='Pull-up exercise',
        #         dificulty_level=2
        #     )

        #     invalid_sets_reps_weight = [
        #         [0, 0, 0],
        #         [-1, -2, -3],
        #         [0, 10, 20],
        #         [3, 0, 20],
        #         [3, 10, 0],
        #         [3, 10, -1],
        #         [3, -1, 20],
        #         [-1, 10, 20],
        #     ]

        #     exceptions_count = 0
        #     for sets, reps, weight in invalid_sets_reps_weight:
        #         try:
        #             models.StrengthExerciseLog.objects.create(
        #                 user=user,
        #                 exercise=strength_exercise,
        #                 sets=sets,
        #                 reps=reps,
        #                 weight=weight,
        #             )
        #         except ValidationError:
        #             exceptions_count += 1
        #     self.assertEqual(exceptions_count, len(invalid_sets_reps_weight)

        # def test_create_StrengthExerciseLog_with_invalid_date(self):
        #     """Test creating a StrengthExerciseLog with invalid date"""

        #     user = create_user()
        #     strength_exercise = models.StrengthExercise.objects.create(
        #         name='Pull-up',
        #         description='Pull-up exercise',
        #         dificulty_level=2
        #     )

        #     invalid_dates = [
        #         datetime.now().date() + timedelta(days=1),
        #         datetime.now().date() - timedelta(days=1),
        #     ]

        #     exceptions_count = 0
        #     for date in invalid_dates:
        #         try:
        #             models.StrengthExerciseLog.objects.create(
        #                 user=user,
        #                 exercise=strength
