# Generated by Django 4.2.13 on 2024-08-16 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0017_alter_student_last_schedule_invite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='last_schedule_invite',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
