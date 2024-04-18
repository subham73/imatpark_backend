"""
Serializers for exercise API
"""
from rest_framework import serializers

from core.models import (
    Exercise,
)


class ExerciseSerializer(serializers.ModelSerializer):
    """ Serializer for Exercise objects"""
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'dificulty_level')
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create and return a new Exercise"""
        exercise = Exercise.objects.create(**validated_data)
        return exercise


class ExerciseDetailSerializer(ExerciseSerializer):
    """ Serializer for exercise detail"""
    class Meta(ExerciseSerializer.Meta):
        '''comma is neccessary here with out it will be a string
          and with, its a tuple eg. ('description', 'image')'''
        fields = ExerciseSerializer.Meta.fields + ('description',)
