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
    TrackExercise,
    StrengthExerciseLog,
)

from exercise import serializers


class BaseExerciseViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the Strength Exercise for the authenticated user"""
        return self.queryset.all().order_by('-id')
        # add distinct at the end and see what happens

    def perform_create(self, serializer):
        """Create a new exercise"""
        serializer.save()


class StrengthExerciseViewSet(BaseExerciseViewSet):
    """Manage exercises in the database"""
    serializer_class = serializers.StrengthExerciseDetailSerializer
    queryset = StrengthExercise.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return serializers.StrengthExerciseSerializer

        return self.serializer_class


class TrackExerciseViewSet(BaseExerciseViewSet):
    serializer_class = serializers.TrackExerciseDetailSerializer
    queryset = TrackExercise.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return serializers.TrackExerciseSerializer

        return self.serializer_class


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


class StrengthExerciseLogViewSet(viewsets.ModelViewSet):
    """Manage exercise logs in the database"""
    serializer_class = serializers.StrengthExerciseLogSerializer
    queryset = StrengthExerciseLog.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the exercise logs for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new exercise log"""
        serializer.save(user=self.request.user)