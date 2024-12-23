import random
from django.db import models
from django.utils.translation import gettext_lazy as _
import timetable.models
from django.conf import settings
from slack_sdk import WebClient
from django.db.models import Q

if settings.SLACK_BOT_TOKEN:
    client = WebClient(token=settings.SLACK_BOT_TOKEN)
# Create your models here.
def get_random_teacher():
    lowest_ref_count = (
    timetable.models.Teacher.objects.filter(type=1).annotate(assigned_count=models.Count('assigned_problems'))
    .aggregate(models.Min('assigned_count'))['assigned_count__min']
)
    if timetable.models.Teacher.objects.filter(type=1).exists():
        objects = list(timetable.models.Teacher.objects.annotate(assigned_count=models.Count("assigned_problems")).filter(type=1,assigned_count=lowest_ref_count))
        return random.choice(objects)
    return None
class problem(models.Model):
    problem = models.CharField(max_length=100)
    room = models.ForeignKey(timetable.models.Room, on_delete=models.CASCADE)
    urgency = models.IntegerField(choices=[(0,_("Take Your Time")),(1,_("Urgent")),(2,_("COME RIGHT NOW!"))],default=0)
    resolved = models.BooleanField(default=False)
    date_reported = models.DateTimeField(auto_now=True)
    reporter = models.ForeignKey(timetable.models.Teacher,related_name="reported_problems",null=True,blank=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(timetable.models.Teacher,limit_choices_to={"type":1},default=get_random_teacher,related_name="assigned_problems", on_delete=models.SET_DEFAULT)
    resolved_by = models.ForeignKey(timetable.models.Teacher,limit_choices_to={"type":1},related_name="resolved_problems",null=True,blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.problem} {_('In')} {self.room}, {_('Reported by')}: {self.reporter}, {_('Assigned to')} {self.assignee}"
    def save(self, *args, **kwargs):
        if client and self.assignee.slack_id:
            client.chat_postMessage(channel=f"{self.assignee.slack_id}",text=f"A New problem has been assigned to you! {self.problem} in {self.room}! The problem was reported by {self.reporter}, he says its {self.urgency}")
        super(problem, self).save(*args, **kwargs)


