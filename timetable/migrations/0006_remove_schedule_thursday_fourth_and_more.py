# Generated by Django 4.2.13 on 2024-08-04 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0005_alter_student_grade_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='thursday_fourth',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='thursday_third',
        ),
    ]
