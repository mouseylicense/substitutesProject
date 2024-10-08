# Generated by Django 4.2.13 on 2024-09-12 07:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LaptopLoaning', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptoppin',
            name='numberOfLaptops',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='laptoppin',
            name='uses',
            field=models.IntegerField(default=2),
        ),
    ]
