"""
Serializers for exercise API
"""
from rest_framework import serializers

from core.models import (
    StrengthExercise,
)


class StrengthExerciseSerializer(serializers.ModelSerializer):
    """ Serializer for Strength Exercise objects"""
    class Meta:
        model = StrengthExercise
        fields = ('id', 'name', 'dificulty_level')
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create and return a new Strength Exercise"""
        exercise = StrengthExercise.objects.create(**validated_data)
        return exercise


class StrengthExerciseDetailSerializer(StrengthExerciseSerializer):
    """ Serializer for strength exercise detail"""
    class Meta(StrengthExerciseSerializer.Meta):
        '''comma is neccessary here with out it will be a string
          and with, its a tuple eg. ('description', 'image')'''
        fields = StrengthExerciseSerializer.Meta.fields + ('description',)
