# Generated by Django 4.2.13 on 2024-09-17 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='has_projector',
        ),
        migrations.AddField(
            model_name='room',
            name='show_as_possible',
            field=models.BooleanField(default=True),
        ),
    ]