# Generated by Django 5.0.9 on 2024-10-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_strengthexerciselog_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trackexercise',
            name='primary_muscle_groups',
        ),
        migrations.RemoveField(
            model_name='trackexercise',
            name='secondary_muscle_groups',
        ),
        migrations.AlterField(
            model_name='strengthexercise',
            name='primary_muscle_groups',
            field=models.ManyToManyField(related_name='primary_muscle_groups', to='core.musclegroup'),
        ),
        migrations.AlterField(
            model_name='strengthexercise',
            name='secondary_muscle_groups',
            field=models.ManyToManyField(related_name='secondary_muscle_groups', to='core.musclegroup'),
        ),
    ]
