"""
Serializers for exercise API
"""
from rest_framework import serializers

from core.models import (
    StrengthExercise,
    MuscleGroup,
    TrackExercise,
    StrengthExerciseLog,
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


class BaseExerciseSerializer(serializers.ModelSerializer):
    """ Base Exercise Serializer"""
    primary_muscle_groups = MuscleGroupSerializer(many=True, required=False)
    secondary_muscle_groups = MuscleGroupSerializer(many=True, required=False)

    class Meta:
        fields = ('id', 'primary_muscle_groups',
                  'secondary_muscle_groups',)
        read_only_fields = ['id']

    def validate(self, data):
        """
        Custom validation to ensure that primary and secondary muscles
        are not the same.
        """
        primary_muscle_groups_data = data.get('primary_muscle_groups', [])
        secondary_muscle_groups_data = data.get('secondary_muscle_groups', [])

        primary_muscle_group_names = set(mg['name'] for mg
                                         in primary_muscle_groups_data)
        secondary_muscle_group_names = set(mg['name'] for mg
                                           in secondary_muscle_groups_data)

        if primary_muscle_group_names & secondary_muscle_group_names:
            raise serializers.ValidationError(
                "Primary and secondary muscle groups must be different.")

        return data

    def _get_or_create_muscle_group(self, muscle_group_data,
                                    field_name,
                                    strength_exercise):
        """Handle getting or creating muscle groups as needed."""
        muscle_group_field = getattr(strength_exercise, field_name)
        for muscle_group_dict in muscle_group_data:
            muscle_group_obj, _ = MuscleGroup.objects.get_or_create(
                **muscle_group_dict
            )
            muscle_group_field.add(muscle_group_obj)

    def create(self, validated_data):
        """Create and return a new Strength Exercise"""
        primary_muscle_group_data = validated_data.pop(
                                                'primary_muscle_groups', [])
        secondary_muscle_group_data = validated_data.pop(
                                                'secondary_muscle_groups', [])

        strength_exercise = self.Meta.model.objects.create(**validated_data)
        self._get_or_create_muscle_group(primary_muscle_group_data,
                                         'primary_muscle_groups',
                                         strength_exercise)
        self._get_or_create_muscle_group(secondary_muscle_group_data,
                                         'secondary_muscle_groups',
                                         strength_exercise)

        return strength_exercise

    def update(self, instance, validated_data):
        """Update and return a Strength Exercise"""
        primary_muscle_group_data = validated_data.pop(
                                            'primary_muscle_groups', [])
        secondary_muscle_group_data = validated_data.pop(
                                            'secondary_muscle_groups', [])

        if primary_muscle_group_data is not None:
            instance.primary_muscle_groups.clear()
            self._get_or_create_muscle_group(primary_muscle_group_data,
                                             'primary_muscle_groups',
                                             instance)
        if secondary_muscle_group_data is not None:
            instance.secondary_muscle_groups.clear()
            self._get_or_create_muscle_group(secondary_muscle_group_data,
                                             'secondary_muscle_groups',
                                             instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class StrengthExerciseSerializer(BaseExerciseSerializer):
    """ Serializer for Strength Exercise objects"""
    class Meta(BaseExerciseSerializer.Meta):
        model = StrengthExercise
        fields = BaseExerciseSerializer.Meta.fields + \
            ('name', 'dificulty_level', )


class StrengthExerciseImageSerializer(StrengthExerciseSerializer):
    """Serializer for uploading images to strength exercise"""
    class Meta(StrengthExerciseSerializer.Meta):
        fields = ('id', 'image', )
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}


class StrengthExerciseDetailSerializer(StrengthExerciseSerializer):
    """ Serializer for strength exercise detail"""
    class Meta(StrengthExerciseSerializer.Meta):
        '''comma is neccessary here with out it will be a string
          and with, its a tuple eg. ('description', 'image')'''
        fields = StrengthExerciseSerializer.Meta.fields + \
            ('description', 'image')


class TrackExerciseSerializer(BaseExerciseSerializer):
    """ Serializer for Track Exercise objects"""
    class Meta(BaseExerciseSerializer.Meta):
        model = TrackExercise
        fields = BaseExerciseSerializer.Meta.fields + ('name', )


class TrackExerciseDetailSerializer(TrackExerciseSerializer):
    """ Serializer for strength exercise detail"""
    class Meta(TrackExerciseSerializer.Meta):
        '''comma is neccessary here with out it will be a string
          and with, its a tuple eg. ('description', 'image')'''
        fields = TrackExerciseSerializer.Meta.fields


class BaseExerciseLogSerializer(serializers.ModelSerializer):
    """Base Exercise Log Serializer"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'user', 'timestamp', 'calories_burned')
        read_only_fields = ['id', 'user', 'timestamp']


class StrengthExerciseLogSerializer(BaseExerciseLogSerializer):
    """Serializer for Strength Exercise Log"""
    exercise = serializers.SlugRelatedField(
        queryset=StrengthExercise.objects.all(),
        slug_field='name'
    )

    class Meta(BaseExerciseLogSerializer.Meta):
        model = StrengthExerciseLog
        fields = BaseExerciseLogSerializer.Meta.fields + \
            ('exercise', 'reps', 'sets', )

    def create(self, validated_data):
        """Create and return a new Strength Exercise Log"""
        strength_exercise_log = self.Meta.model.objects.create(
                                **validated_data)
        return strength_exercise_log

    def update(self, instance, validated_data):
        """Update and return a Strength Exercise Log"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
