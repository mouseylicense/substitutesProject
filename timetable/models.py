from django.db import models
import datetime
from django.utils import timezone

DAYS_OF_WEEKDAY = {
    "Sunday": 'Sunday',
    "Monday": 'Monday',
    "Tuesday": 'Tuesday',
    "Wednesday": 'Wednesday',
    "Thursday": 'Thursday'
}


# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    last_sub = models.DateField(default=timezone.now)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Absence(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day = models.DateField()
    reason = models.CharField(max_length=100)


class Class(models.Model):
    name = models.CharField(max_length=100)
    day_of_week = models.CharField(default="", max_length=100, choices=DAYS_OF_WEEKDAY)
    hour = models.fields.TimeField(choices={datetime.time(8,30):"08:30",datetime.time(9,15):"09:15",datetime.time(10,7):"10:07",datetime.time(11,0):"11:00",datetime.time(11,45):"11:45",datetime.time(12,45):"12:45",datetime.time(13,45):"13:45"})
    duration = models.fields.DurationField(default=datetime.timedelta(days=0, minutes=45))
    room = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.hour)[:5] + " - " + str(
            (datetime.datetime.combine(datetime.date(1, 1, 1), self.hour) + self.duration).time())[
                                            :5] + " --- " + self.name + " - " + self.teacher.name
