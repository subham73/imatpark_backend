"""
Database Models
"""
# import uuid
# import os

# from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import datetime
current_year = datetime.now().year


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and returns a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    height = models.PositiveIntegerField(
        default=160,
        validators=[
            MinValueValidator(50),
            MaxValueValidator(300)
        ],
        error_messages={
            'min_value': 'Height must be at least 50.',
            'max_value': 'Height cannot exceed 300.',
        }
    )
    weight = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(20), MaxValueValidator(600)],
        error_messages={
            'min_value': 'Weight must be at least 20.',
            'max_value': 'Weight cannot exceed 600.',
        }
    )
    year_of_birth = models.PositiveIntegerField(
        default=2000,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(current_year-5)
        ],
        error_messages={
            'min_value': 'Year of birth must be at least 1900.',
            'max_value': 'you must be at least 5 years old.',
        }
    )
    is_active = models.BooleanField(default=True)  # can login
    is_staff = models.BooleanField(default=False)  # staff user

    objects = UserManager()
    USERNAME_FIELD = 'email'  # default username field


class StrengthExercise(models.Model):
    """Strength Exercise model"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    dificulty_level = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        error_messages={
            'min_value': 'Dificulty level must be at least 1.',
            'max_value': 'Dificulty level cannot exceed 3.',
        }
    )

    def __str__(self):
        return self.name
