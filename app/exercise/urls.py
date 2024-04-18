"""
URL mapping for exercise app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exercise import views

router = DefaultRouter()

router.register('exercise', views.ExerciseViewSet)

app_name = 'exercise'

urlpatterns = [
    path('', include(router.urls)),
]
