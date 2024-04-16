# Generated by Django 5.0.4 on 2024-04-16 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='height',
            field=models.PositiveIntegerField(default=160),
        ),
        migrations.AddField(
            model_name='user',
            name='weight',
            field=models.PositiveIntegerField(default=60),
        ),
    ]
