from random import randint

from django.db import models

import timetable.models


def generate_pin():
    return ''.join(str(randint(0, 9)) for _ in range(4))
# Create your models here.
class LaptopPin(models.Model):
    Teacher = models.ForeignKey(timetable.models.Teacher, on_delete=models.CASCADE)
    PIN = models.CharField(max_length=4, default=generate_pin, unique=True)
    date = models.DateField()