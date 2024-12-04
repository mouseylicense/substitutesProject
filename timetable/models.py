import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

from django.db.models import Exists, OuterRef, Q
from django.template.defaultfilters import first
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
    (0, _('First Grade')),
    (1, _('Second Grade')),
    (2, _('Third Grade')),
    (3, _('Fourth Grade')),
    (4, _('Fifth Grade')),
    (5, _('Sixth Grade')),
    (6, _('Seventh Grade')),
    (7, _('Eighth Grade')),
    (8, _('Ninth Grade')),
    (9, _('Tenth Grade')),
    (10, _('Eleventh Grade')),
    (11, _('Twelfth Grade')),
]

class TeacherManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None,**extra_fields):

        if not email:
            raise ValueError('Email must be set')
        if not first_name:
            raise ValueError('First Name must be set')
        if not last_name:
            raise ValueError('Last Name must be set')
        teacher = Teacher(email=email,first_name=first_name,last_name=last_name, **extra_fields)
        if password:
            teacher.set_password(password)
        else:
            teacher.set_unusable_password()
        teacher.save(using=self._db)
        return teacher

    def create_superuser(self,email,first_name,last_name,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        teacher = self.create_user(email,first_name,last_name,password,**extra_fields)
        return teacher

class Teacher(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = None
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=100, unique=True)
    can_substitute = models.BooleanField(default=True)
    Sunday = models.BooleanField(default=True)
    Monday = models.BooleanField(default=True)
    Tuesday = models.BooleanField(default=True)
    Wednesday = models.BooleanField(default=True)
    Thursday = models.BooleanField(default=True)
    tutor = models.BooleanField(default=False)
    shocher = models.BooleanField(default=False)
    manage_subs = models.BooleanField(default=False)
    manage_schedule = models.BooleanField(default=False)
    last_sub = models.DateField(default=timezone.now)
    type = models.IntegerField(choices=[(0,"Teacher"),(1,"TED"),(2,"Management")],default=0)
    objects = TeacherManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        return self.email
    def name(self):
        return self.first_name + " " + self.last_name



class Room(models.Model):
    name = models.CharField(max_length=100)
    show_as_possible = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    def get_class(self,time,day):
            t = self.class_set.filter(day_of_week=day,hour__in=['9:15', '10:07', '11:00', '11:45', '12:45', '13:45'],hour__lte=time).order_by('-hour').first()
            if t == None:
                return _("Empty")
            return t.name
class Absence(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=100)
    def date_str(self):
        return str(self.date)
    def __str__(self):
        return self.teacher.first_name + " - " + str(self.date)


# removes classes that needs sub if absence is deleted
@receiver(post_delete, sender=Absence)
def remove_classes(sender, instance, using, **kwargs):
    c = ClassNeedsSub.objects.filter(Class_That_Needs_Sub__teacher=instance.teacher, date=instance.date).delete()
    print(c)


class Class(models.Model):
    name = models.CharField(max_length=100)
    day_of_week = models.CharField(default="", max_length=100, choices=DAYS_OF_WEEKDAY)
    hour = models.fields.TimeField(
        choices=[ (datetime.time(9, 15), "09:15"), (datetime.time(10, 7), "10:07"),
                 (datetime.time(11, 0), "11:00"), (datetime.time(11, 45), "11:45"), (datetime.time(12, 45), "12:45")])
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
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
    visible = models.BooleanField(default=True, verbose_name=_("Visible"))
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
            return str(self.hour)[:5] + " --- " + self.name + " - " + self.teacher.first_name + " " + self.teacher.last_name
        else:
            return str(self.hour)[:5] + " --- " + self.name + " - " + self.student_teaching


class ClassNeedsSub(models.Model):
    related_absence = models.ForeignKey(Absence,null=True,blank=True, on_delete=models.CASCADE)
    Class_That_Needs_Sub = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    substitute_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        permissions = (
            ("see_subs", "can Set Substitutions"),
        )
    def possible_subs(self):
        c = self
        filter_dict = {DAYS_OF_WEEKDAY_DICT[c.date.weekday()]: True}
        teacherQuery = Teacher.objects.filter(
            ~Exists(Class.objects.filter(teacher=OuterRef("pk"), day_of_week=DAYS_OF_WEEKDAY_DICT[c.date.weekday()],
                                         hour=c.Class_That_Needs_Sub.hour)),
            ~Exists(ClassNeedsSub.objects.filter(substitute_teacher=OuterRef("pk"), date=c.date,
                                                 Class_That_Needs_Sub__hour=c.Class_That_Needs_Sub.hour)),
            ~Q(absence__date=c.date),
            can_substitute=True,
            **filter_dict).values("pk", "first_name")
        availableTeachers = []
        for teacher in teacherQuery:
            availableTeachers.append({'id': teacher['pk'], 'name': teacher['first_name']})
        return availableTeachers
    def __str__(self):
        if self.substitute_teacher is None:
            return str(self.date) + " - " + str(self.Class_That_Needs_Sub)
        else:
            return "✔ " + str(self.date) + " - " + str(self.Class_That_Needs_Sub.hour) + " " + str(
                self.Class_That_Needs_Sub.name) + " Sub:" + str(self.substitute_teacher.first_name)


class Student(models.Model):
    name = models.CharField(max_length=50)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    grade = models.IntegerField(choices=GRADES, default="")
    tutor = models.ForeignKey(Teacher, on_delete=models.SET_NULL, limit_choices_to={'tutor': True}, null=True,
                              blank=True)
    shacharit = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True,
                                  limit_choices_to={'shocher': True}, related_name="shacharit")
    last_schedule_invite = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.name
    def increment_grade(self):
        if self.grade == 11:
            self.delete()
        else:
            self.grade = self.grade + 1
            self.save()

    def str_grades(self):
        number_to_grade = {
            0: _("First Grade"),
            1: _("Second Grade"),
            2: _("Third Grade"),
            3: _("Fourth Grade"),
            4: _("Fifth Grade"),
            5: _("Sixth Grade"),
            6: _("Seventh Grade"),
            7: _("Eighth Grade"),
            8: _("Ninth Grade"),
            9: _("Tenth Grade"),
            10: _("Eleventh Grade"),
            11: _("Twelfth Grade"),
        }
        return number_to_grade[self.grade]

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

