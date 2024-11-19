# Generated by Django 4.2.13 on 2024-11-18 17:23

import dashboard.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='assignee',
            field=models.ForeignKey(default=dashboard.models.get_random_teacher, limit_choices_to={'type': 1}, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_problems', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='problem',
            name='reporter',
            field=models.ForeignKey(limit_choices_to=models.Q(('type', 0), ('type', 2), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='reported_problems', to=settings.AUTH_USER_MODEL),
        ),
    ]
