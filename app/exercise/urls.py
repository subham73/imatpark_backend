"""
URL mapping for exercise app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exercise import views

router = DefaultRouter()

router.register('strength-exercise',
                views.StrengthExerciseViewSet,
                basename='strength-exercise')
router.register('muscle-group',
                views.MuscleGroupViewSet,
                basename='muscle-group')
router.register('track-exercise',
                views.TrackExerciseViewSet,
                basename='track-exercise')
router.register('strength-exercise-log',
                views.StrengthExerciseLogViewSet,
                basename='strength-exercise-log')

app_name = 'exercise'

urlpatterns = [
    path('', include(router.urls)),
]
