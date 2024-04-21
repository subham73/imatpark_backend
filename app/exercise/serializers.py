"""
Serializers for exercise API
"""
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from core.models import (
    StrengthExercise,
    MuscleGroup,
)


class MuscleGroupSerializer(serializers.ModelSerializer):
    """ Serializer for Muscle Group objects"""
    class Meta:
        model = MuscleGroup
        fields = ('id', 'name', )
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'validators': []},
        }


class StrengthExerciseSerializer(serializers.ModelSerializer):
    """ Serializer for Strength Exercise objects"""
    primary_muscle_groups = MuscleGroupSerializer(many=True, required=False)
    class Meta:
        model = StrengthExercise
        fields = ('id', 'name', 'dificulty_level', 'primary_muscle_groups')
        read_only_fields = ['id']

    def _get_or_create_muscle_group(self, muscle_group_data, field_name, strength_exercise):
        """Handle getting or creating muscle groups as needed."""
        muscle_group_field = getattr(strength_exercise, field_name)
        for muscle_group_dict in muscle_group_data:
            muscle_group_obj, _ = MuscleGroup.objects.get_or_create(
                **muscle_group_dict
            )
            muscle_group_field.add(muscle_group_obj)

    def create(self, validated_data):
        """Create and return a new Strength Exercise"""
        primary_muscle_group_data = validated_data.pop('primary_muscle_groups', [])

        strength_exercise = StrengthExercise.objects.create(**validated_data)
        self._get_or_create_muscle_group(primary_muscle_group_data, 'primary_muscle_groups', strength_exercise)

        return strength_exercise

    def update(self, instance, validated_data):
        """Update and return a Strength Exercise"""
        primary_muscle_group_data = validated_data.pop('primary_muscle_groups', [])

        if primary_muscle_group_data is not None:
            instance.primary_muscle_groups.clear()
            self._get_or_create_muscle_group(primary_muscle_group_data, 'primary_muscle_groups', instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class StrengthExerciseDetailSerializer(StrengthExerciseSerializer):
    """ Serializer for strength exercise detail"""
    class Meta(StrengthExerciseSerializer.Meta):
        '''comma is neccessary here with out it will be a string
          and with, its a tuple eg. ('description', 'image')'''
        fields = StrengthExerciseSerializer.Meta.fields + ('description', )
