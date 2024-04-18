"""
Views for the exercise APIs
"""
# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
#     OpenApiParameter,
#     OpenApiTypes,
# )
from rest_framework import (
    viewsets,
    # mixins,
    # status,
)
# from rest_framework.decorators import action
# from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Exercise,
)

from exercise import serializers


class ExerciseViewSet(viewsets.ModelViewSet):
    """Manage exercises in the database"""
    serializer_class = serializers.ExerciseSerializer
    queryset = Exercise.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return serializers.ExerciseSerializer
        else:
            return serializers.ExerciseDetailSerializer

    # def get_queryset(self):
    #     """Retrieve the exercises for the authenticated user"""
    #     return self.queryset.filter(user=self.request.user).order_by('-id')

    # def perform_create(self, serializer):
    #     """Create a new exercise"""
    #     serializer.save(user=self.request.user)
