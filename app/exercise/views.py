"""
Views for the exercise APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    # status,
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    StrengthExercise,
    MuscleGroup,
)

from exercise import serializers


class StrengthExerciseViewSet(viewsets.ModelViewSet):
    """Manage exercises in the database"""
    serializer_class = serializers.StrengthExerciseDetailSerializer
    queryset = StrengthExercise.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the Strength Exercise for the authenticated user"""
        return self.queryset.all().order_by('-id')  #add distinct and see what happens

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return serializers.StrengthExerciseSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new exercise"""
        serializer.save()


class MuscleGroupViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Manage muscle groups in the database"""
    serializer_class = serializers.MuscleGroupSerializer
    queryset = MuscleGroup.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the muscle groups for the authenticated user"""
        return self.queryset.all()
