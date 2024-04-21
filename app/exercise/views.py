"""
Views for the exercise APIs
"""
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    viewsets,
    mixins,
    # status,
)
# from rest_framework.decorators import action
# from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    StrengthExercise,
    MuscleGroup,
)

from exercise import serializers

# @extend_schema_view(
#     list=extend_schema(
#         parameteres=[
#             OpenApiParameter(
#                 name='name',
#                 type=OpenApiTypes.STR,
#                 description='Filter by name',
#             ),
#         ]
#     )
# )
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
        return self.queryset.all().order_by('-name')


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
