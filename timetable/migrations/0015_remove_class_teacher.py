# Generated by Django 4.2.13 on 2024-12-29 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0014_auto_20241229_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='teacher',
        ),
    ]
