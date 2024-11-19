import random
from django.db import models
from django.utils.translation import gettext_lazy as _
import timetable.models
from django.db.models import Q
# Create your models here.
def get_random_teacher():
    lowest_ref_count = (
    timetable.models.Teacher.objects.annotate(assigned_count=models.Count('assigned_problems'))
    .aggregate(models.Min('assigned_count'))['assigned_count__min']
)
    objects = list(timetable.models.Teacher.objects.annotate(assigned_count=models.Count("assigned_problems")).filter(type=1,assigned_count=lowest_ref_count))
    return random.choice(objects)
class problem(models.Model):
    problem = models.CharField(max_length=100)
    room = models.ForeignKey(timetable.models.Room, on_delete=models.CASCADE)
    urgency = models.IntegerField(choices=[(0,_("Take Your Time")),(1,_("Urgent")),(2,_("COME RIGHT NOW!"))],default=0)
    resolved = models.BooleanField(default=False)
    date_reported = models.DateTimeField(auto_now=True)
    reporter = models.ForeignKey(timetable.models.Teacher,related_name="reported_problems",null=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(timetable.models.Teacher,limit_choices_to={"type":1},default=get_random_teacher,related_name="assigned_problems", on_delete=models.SET_DEFAULT)
    resolved_by = models.ForeignKey(timetable.models.Teacher,limit_choices_to={"type":1},related_name="resolved_problems",null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.problem} {_('In')} {self.room}, {_('Reported by')}: {self.reporter}, {_('Assigned to')} {self.assignee}"