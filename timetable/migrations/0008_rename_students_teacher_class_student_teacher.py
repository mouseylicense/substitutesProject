# Generated by Django 4.2.13 on 2024-07-14 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0007_alter_class_student_teaching_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='students_teacher',
            new_name='student_teacher',
        ),
    ]