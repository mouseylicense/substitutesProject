# Generated by Django 4.2.13 on 2024-12-22 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0005_class_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='slack_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]