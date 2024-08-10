import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

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
    ("Wednesday", 'Wednesday'),
    ("Thursday", 'Thursday')
]
GRADES = [
    (0, 'First Grade'),
    (1, 'Second Grade'),
    (2, 'Third Grade'),
    (3, 'Fourth Grade'),
    (4, 'Fifth Grade'),
    (5, 'Sixth Grade'),
    (6, 'Seventh Grade'),
    (7, 'Eighth Grade'),
    (8, 'Ninth Grade'),
    (9, 'Tenth Grade'),
    (10, 'Eleventh Grade'),
    (11, 'Twelfth Grade'),
    (12, 'Graduate')
]



# Create your models here.
class Teacher(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(max_length=100, unique=True, verbose_name="name")
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    can_substitute = models.BooleanField(default=True)
    Sunday = models.BooleanField(default=True)
    Monday = models.BooleanField(default=True)
    Tuesday = models.BooleanField(default=True)
    Wednesday = models.BooleanField(default=True)
    Thursday = models.BooleanField(default=True)
    tutor = models.BooleanField(default=False)
    shocher = models.BooleanField(default=False)
    last_sub = models.DateField(default=timezone.now)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__(self):
        return self.username


class Room(models.Model):
    name = models.CharField(max_length=100)
    has_projector = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Absence(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=100)

    def __str__(self):
        return self.teacher.username + " - " + str(self.date)


# removes classes that needs sub if absence is deleted
@receiver(post_delete, sender=Absence)
def remove_classes(sender, instance, using, **kwargs):
    c = ClassNeedsSub.objects.filter(substitute_teacher=instance.teacher, date=instance.date)
    for i in c:
        i.delete()
        i.save()


class Class(models.Model):
    name = models.CharField(max_length=100)
    day_of_week = models.CharField(default="", max_length=100, choices=DAYS_OF_WEEKDAY)
    hour = models.fields.TimeField(
        choices=[(datetime.time(8, 30), "08:30"), (datetime.time(9, 15), "09:15"), (datetime.time(10, 7), "10:07"),
                 (datetime.time(11, 0), "11:00"), (datetime.time(11, 45), "11:45"), (datetime.time(12, 45), "12:45"),
                 (datetime.time(13, 45), "13:45")])
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    student_teacher = models.BooleanField(default=False, verbose_name=_("Is a Student Teaching?"))
    student_teaching = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Student Teaching"))
    first_grade = models.BooleanField(default=False, verbose_name=_("First Grade"))
    second_grade = models.BooleanField(default=False, verbose_name=_("Second Grade"))
    third_grade = models.BooleanField(default=False, verbose_name=_("Third Grade"))
    fourth_grade = models.BooleanField(default=False, verbose_name=_("Fourth Grade"))
    fifth_grade = models.BooleanField(default=False, verbose_name=_("Fifth Grade"))
    sixth_grade = models.BooleanField(default=False, verbose_name=_("Sixth Grade"))
    seventh_grade = models.BooleanField(default=False, verbose_name=_("Seventh Grade"))
    eighth_grade = models.BooleanField(default=False, verbose_name=_("Eighth Grade"))
    ninth_grade = models.BooleanField(default=False, verbose_name=_("Ninth Grade"))
    tenth_grade = models.BooleanField(default=False, verbose_name=_("Tenth Grade"))
    eleventh_grade = models.BooleanField(default=False, verbose_name=_("Eleventh Grade"))
    twelfth_grade = models.BooleanField(default=False, verbose_name=_("Twelfth Grade"))

    class Meta:
        permissions = (
            ('see_classes', "can add classes"),
        )

    def who_teaches(self):
        if self.student_teacher:
            return self.student_teaching
        return self.teacher
    def all_grades(self):
        grades = [self.first_grade, self.second_grade, self.third_grade, self.fourth_grade, self.fifth_grade,
                  self.sixth_grade, self.seventh_grade, self.eighth_grade, self.ninth_grade, self.tenth_grade,
                  self.eleventh_grade, self.twelfth_grade]
        i = 1
        grades_positive = []
        for grade in grades:
            if grade:
                grades_positive.append(i)
            i += 1
        return grades_positive

    def str_grades(self):
        number_to_grade = {
            1: _("First Grade"),
            2: _("Second Grade"),
            3: _("Third Grade"),
            4: _("Fourth Grade"),
            5: _("Fifth Grade"),
            6: _("Sixth Grade"),
            7: _("Seventh Grade"),
            8: _("Eighth Grade"),
            9: _("Ninth Grade"),
            10: _("Tenth Grade"),
            11: _("Eleventh Grade"),
            12: _("Twelfth Grade"),
        }
        grades = [self.first_grade, self.second_grade, self.third_grade, self.fourth_grade, self.fifth_grade,
                  self.sixth_grade, self.seventh_grade, self.eighth_grade, self.ninth_grade, self.tenth_grade,
                  self.eleventh_grade, self.twelfth_grade]

        if True in grades:
            rev = grades.copy()
            rev.reverse()
            last_occurrence = len(grades) - rev.index(True)
            first_occurrence = grades.index(True) + 1
            if last_occurrence == first_occurrence:
                return number_to_grade[first_occurrence]
            first_and_last = str(number_to_grade[first_occurrence]) + " - " + str(number_to_grade[last_occurrence])
            return first_and_last
        return None

    def __str__(self):
        if self.teacher:
            return str(self.hour)[:5] + " --- " + self.name + " - " + self.teacher.username
        else:
            return str(self.hour)[:5] + " --- " + self.name + " - " + self.student_teaching


class ClassNeedsSub(models.Model):
    Class_That_Needs_Sub = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    substitute_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        permissions = (
            ("see_subs", "can Set Substitutions"),
        )

    def __str__(self):
        if self.substitute_teacher is None:
            return str(self.date) + " - " + str(self.Class_That_Needs_Sub)
        else:
            return "✔ " + str(self.date) + " - " + str(self.Class_That_Needs_Sub.hour) + " " + str(
                self.Class_That_Needs_Sub.name) + " Sub:" + str(self.substitute_teacher.username)


class Student(models.Model):
    name = models.CharField(max_length=50)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    grade = models.IntegerField(choices=GRADES, default="")
    tutor = models.ForeignKey(Teacher, on_delete=models.CASCADE, limit_choices_to={'tutor': True}, null=True,
                              blank=True)
    shacharit = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True,
                                  limit_choices_to={'shocher': True}, related_name="shacharit")
    last_schedule_invite = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.name

class Schedule(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    sunday_first = models.ForeignKey(Class,verbose_name=_("Sunday") + " 09:15", on_delete=models.SET_NULL, null=True, blank=True,
                                     limit_choices_to={'day_of_week': "Sunday", "hour": datetime.time(9, 15),
                                                       }, related_name='sunday_first_classes')
    sunday_second = models.ForeignKey(Class,verbose_name=_("Sunday") + " 10:07", on_delete=models.SET_NULL, null=True, blank=True,
                                      limit_choices_to={'day_of_week': "Sunday", "hour": datetime.time(10, 7),
                                                        }, related_name='sunday_second_classes')
    sunday_third = models.ForeignKey(Class,verbose_name=_("Sunday") + " 11:45", on_delete=models.SET_NULL, null=True, blank=True,
                                     limit_choices_to={'day_of_week': "Sunday", "hour": datetime.time(11, 45),
                                                       }, related_name='sunday_third_classes')
    sunday_fourth = models.ForeignKey(Class,verbose_name=_("Sunday") + " 12:45", on_delete=models.SET_NULL, null=True, blank=True,
                                      limit_choices_to={'day_of_week': "Sunday", "hour": datetime.time(12, 45),
                                                        }, related_name='sunday_fourth_classes')
    monday_first = models.ForeignKey(Class,verbose_name=_("Monday") + " 09:15", on_delete=models.SET_NULL, null=True, blank=True,
                                     limit_choices_to={'day_of_week': "Monday", "hour": datetime.time(9, 15),
                                                       }, related_name='monday_first_classes')
    monday_second = models.ForeignKey(Class,verbose_name=_("Monday") + " 10:07", on_delete=models.SET_NULL, null=True, blank=True,
                                      limit_choices_to={'day_of_week': "Monday", "hour": datetime.time(10, 7),
                                                        }, related_name='monday_second_classes')
    monday_third = models.ForeignKey(Class,verbose_name=_("Monday") + " 11:45", on_delete=models.SET_NULL, null=True, blank=True,
                                     limit_choices_to={'day_of_week': "Monday", "hour": datetime.time(11, 45),
                                                       }, related_name='monday_third_classes')
    monday_fourth = models.ForeignKey(Class,verbose_name=_("Monday") + " 12:45", on_delete=models.SET_NULL, null=True, blank=True,
                                      limit_choices_to={'day_of_week': "Monday", "hour": datetime.time(12, 45),
                                                        }, related_name='monday_fourth_classes')
    tuesday_first = models.ForeignKey(Class, verbose_name=_("Tuesday") + " 09:15",on_delete=models.SET_NULL, null=True, blank=True,
                                      limit_choices_to={'day_of_week': "Tuesday", "hour": datetime.time(9, 15),
                                                        }, related_name='tuesday_first_classes')
    tuesday_second = models.ForeignKey(Class,verbose_name=_("Tuesday") + " 10:07", on_delete=models.SET_NULL, null=True, blank=True,
                                       limit_choices_to={'day_of_week': "Tuesday", "hour": datetime.time(10, 7),
                                                         },
                                       related_name='tuesday_second_classes')
    tuesday_third = models.ForeignKey(Class,verbose_name=_("Tuesday") + " 11:45", on_delete=models.SET_NULL, null=True, blank=True,
                                      limit_choices_to={'day_of_week': "Tuesday", "hour": datetime.time(11, 45),
                                                        }, related_name='tuesday_third_classes')
    tuesday_fourth = models.ForeignKey(Class, verbose_name=_("Tuesday") + " 12:45",on_delete=models.SET_NULL, null=True, blank=True,
                                       limit_choices_to={'day_of_week': "Tuesday", "hour": datetime.time(12, 45),
                                                         },
                                       related_name='tuesday_fourth_classes')
    wednesday_first = models.ForeignKey(Class,verbose_name=_("Wednesday") + " 09:15", on_delete=models.SET_NULL, null=True, blank=True,
                                        limit_choices_to={'day_of_week': "Wednesday", "hour": datetime.time(9, 15),
                                                          },
                                        related_name='wednesday_first_classes')
    wednesday_second = models.ForeignKey(Class,verbose_name=_("Wednesday") + " 10:07", on_delete=models.SET_NULL, null=True, blank=True,
                                         limit_choices_to={'day_of_week': "Wednesday", "hour": datetime.time(10, 7),
                                                           },
                                         related_name='wednesday_second_classes')
    wednesday_third = models.ForeignKey(Class,verbose_name=_("Wednesday") + " 11:45", on_delete=models.SET_NULL, null=True, blank=True,
                                        limit_choices_to={'day_of_week': "Wednesday", "hour": datetime.time(11, 45),
                                                          },
                                        related_name='wednesday_third_classes')
    wednesday_fourth = models.ForeignKey(Class,verbose_name=_("Wednesday") + " 12:45", on_delete=models.SET_NULL, null=True, blank=True,
                                         limit_choices_to={'day_of_week': "Wednesday", "hour": datetime.time(12, 45),
                                                           },
                                         related_name='wednesday_fourth_classes')
    thursday_first = models.ForeignKey(Class, verbose_name=_("Thursday") + " 09:15",on_delete=models.SET_NULL, null=True, blank=True,
                                       limit_choices_to={'day_of_week': "Thursday", "hour": datetime.time(9, 15),
                                                         },
                                       related_name='thursday_first_classes')
    thursday_second = models.ForeignKey(Class,verbose_name=_("Thursday") + " 10:07", on_delete=models.SET_NULL, null=True, blank=True,
                                        limit_choices_to={'day_of_week': "Thursday", "hour": datetime.time(10, 7),
                                                          },
                                        related_name='thursday_second_classes')
    def __str__(self):
        return self.student.name + " Schedule"

