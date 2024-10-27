from random import randint

from django.core.validators import MinValueValidator
from django.db import models

import timetable.models


def generate_pin():
    return ''.join(str(randint(0, 9)) for _ in range(4))


# Create your models here.
class LaptopPin(models.Model):
    Teacher = models.ForeignKey(timetable.models.Teacher, on_delete=models.CASCADE)
    PIN = models.CharField(max_length=4, default=generate_pin, unique=True)
    date = models.DateField()
    room = models.ForeignKey(timetable.models.Room, on_delete=models.CASCADE)
    uses = models.IntegerField(default=2)
    numberOfLaptops = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    granted = models.BooleanField(default=False)
    def use(self):
        self.uses = self.uses - 1
        if self.uses <= 0:
            self.delete()
        else:
            self.save()

    def __str__(self):
        return f"{self.Teacher} - {self.PIN} - {self.date}"