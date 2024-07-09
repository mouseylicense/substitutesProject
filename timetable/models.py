from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.utils import timezone
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db.models import Q

from SubtitutesProject import settings
DAYS_OF_WEEKDAY_DICT = {
    6: 'Sunday',
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday'
}
DAYS_OF_WEEKDAY = [
    ("Sunday", 'Sunday'),
("Monday", 'Monday'),
("Tuesday", 'Tuesday'),
("Wednesday",'Wednesday'),
    ("Thursday", 'Thursday')
]


# Create your models here.
class Teacher(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(max_length=100,unique=True,verbose_name="name")
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    can_substitute = models.BooleanField(default=True)
    Sunday = models.BooleanField(default=True)
    Monday = models.BooleanField(default=True)
    Tuesday = models.BooleanField(default=True)
    Wednesday = models.BooleanField(default=True)
    Thursday = models.BooleanField(default=True)
    last_sub = models.DateField(default=timezone.now)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone_number']
    def __str__(self):
        return self.username


class Absence(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=100)
    def __str__(self):
        return self.teacher.username + " - " + str(self.date)


#removes classes that needs sub if absence is deleted
@receiver(post_delete,sender=Absence)
def remove_classes(sender, instance,using, **kwargs):
    c = ClassNeedsSub.objects.filter(teacher=instance.teacher,date=instance.date)
    for i in c:
        i.delete()
        i.save()


class Class(models.Model):
    name = models.CharField(max_length=100)
    day_of_week = models.CharField(default="", max_length=100, choices=DAYS_OF_WEEKDAY)
    hour = models.fields.TimeField(choices=[(datetime.time(8,30),"08:30"),(datetime.time(9,15),"09:15"),(datetime.time(10,7),"10:07"),(datetime.time(11,0),"11:00"),(datetime.time(11,45),"11:45"),(datetime.time(12,45),"12:45"),(datetime.time(13,45),"13:45")])
    duration = models.fields.DurationField(default=datetime.timedelta(days=0, minutes=45))
    room = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)



    def __str__(self):
        return str(self.hour)[:5] + " - " + str(
            (datetime.datetime.combine(datetime.date(1, 1, 1), self.hour) + self.duration).time())[
                                            :5] + " --- " + self.name + " - " + self.name


class ClassNeedsSub(models.Model):
    Class_That_Needs_Sub = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    substitute_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        if self.substitute_teacher is None:
            return str(self.date) + " - " + str(self.Class_That_Needs_Sub)
        else:
            return "✔ " + str(self.date) + " - " + str(self.Class_That_Needs_Sub.hour) + " " + str(self.Class_That_Needs_Sub.name) + " Sub:" + str(self.substitute_teacher.name)