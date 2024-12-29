import json
import random
from django.db import models
from django.utils.translation import gettext_lazy as _
import timetable.models
from django.conf import settings
from slack_sdk import WebClient
import constance
URGENCY_DICT = {0:"Not that urgent",
                1:"Urgent",
                2:"VERY URGENT!"}
if hasattr(settings, 'SLACK_BOT_TOKEN'):
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


# noinspection ConstanceSettingUsageInspection
class problem(models.Model):
    problem = models.CharField(max_length=100)
    room = models.ForeignKey(timetable.models.Room, on_delete=models.CASCADE)
    urgency = models.IntegerField(choices=[(0,_("Take Your Time")),(1,_("Urgent")),(2,_("COME RIGHT NOW!"))],default=0)
    resolved = models.BooleanField(default=False)
    date_reported = models.DateTimeField(auto_now=True)
    reporter = models.ForeignKey(timetable.models.Teacher,related_name="reported_problems",null=True,blank=True, on_delete=models.SET_NULL)
    reporter_guest = models.CharField(max_length=100,blank=True)
    assignee = models.ForeignKey(timetable.models.Teacher,limit_choices_to={"type":1},default=get_random_teacher,related_name="assigned_problems", on_delete=models.SET_DEFAULT)
    resolved_by = models.ForeignKey(timetable.models.Teacher,limit_choices_to={"type":1},related_name="resolved_problems",null=True,blank=True, on_delete=models.SET_NULL)
    public_ts = models.CharField(max_length=100,blank=True)
    private_ts = models.CharField(max_length=100,blank=True)
    private_id = models.CharField(max_length=100,blank=True)
    def name(self):
        if self.reporter:
            return self.reporter.name()
        else:
            return self.reporter_guest
    def __str__(self):
        return f"{self.problem} {_('In')} {self.room}, {_('Reported by')}: {self.name()}, {_('Assigned to')} {self.assignee}"
    def resolve(self,user):
        self.resolved = True
        self.resolved_by = user
        self.save()
        try:
            if self.assignee.slack_id and self.resolved_by.slack_id:
                client.chat_update(ts=self.public_ts, channel=constance.config.SLACK_PROBLEMS_CHANNEL_ID,
                                   text=f"~A new Problem has been assigned to <@{self.assignee.slack_id}>! {self.problem} in {self.room}! The problem was reported by {self.name()}, he says its {URGENCY_DICT[self.urgency]}~ \n\n Problem Fixed by <@{user.slack_id}>.")
                client.chat_update(ts=self.private_ts, channel=self.private_id,
                                   text=f"~A New problem has been assigned to you! {self.problem} in {self.room}! The problem was reported by {self.name()}, he says its {URGENCY_DICT[self.urgency]}~ \n\n Problem Fixed by <@{user.slack_id}>.")
        except NameError:
            print("No client")
    def save(self, *args, **kwargs):
        super(problem, self).save(*args, **kwargs)
        try:
            if client and self.assignee.slack_id and self.resolved == False:
                blocks_private = [
        {
            "text": {
                "text": f"A New problem has been assigned to you! {self.problem} in {self.room}! The problem was reported by {self.name()}, he says its {URGENCY_DICT[self.urgency]}",
                "type": "mrkdwn"
            },
            "type": "section"
        }, {
            "type":"actions",
            "block_id":"resolve",
            "elements":[{
                "type": "button",
                "style": "primary",
                "text": {
                    "type": "plain_text",
                    "text": "Resolve",
                },
                "value": f"{self.id}",
                "action_id": "resolve"
            }]}
    ]
                blocks_public = [
        {
            "text": {
                "text": f"A new Problem has been assigned to <@{self.assignee.slack_id}>! {self.problem} in {self.room}! The problem was reported by {self.name()}, he says its {URGENCY_DICT[self.urgency]}",
                "type": "mrkdwn"
            },
            "type": "section"
        }, {
            "type":"actions",
            "block_id":"resolve",
            "elements":[{
                "type": "button",
                "style": "primary",
                "text": {
                    "type": "plain_text",
                    "text": "Resolve",
                },
                "value": f"{self.id}",
                "action_id": "resolve"
            }]}
    ]
                # change to urgent text if problem is very urgent
                if self.urgency == 2:
                    blocks_public[0]["text"][
                        "text"] = f"<!channel> A new VERY URGENT Problem has been assigned to <@{self.assignee.slack_id}>! {self.problem} in {self.room}! The problem was reported by {self.name()}"

                # if the problem is reassigned, delete old dm
                if self.private_ts:
                    client.chat_delete(channel=self.private_id,ts=self.private_ts)
                # if problem is reassigned, update old message to new assignee instead of sending a new message
                if self.public_ts:

                    if self.urgency == 2:
                        client.chat_update(channel=constance.config.SLACK_PROBLEMS_CHANNEL_ID,ts=self.public_ts,
                                                    text=f"<!channel> A new VERY URGENT Problem has been assigned to <@{self.assignee.slack_id}>! {self.problem} in {self.room}! The problem was reported by {self.name()}",
                                           blocks=blocks_public)
                    else:
                        client.chat_update(ts=self.public_ts,channel=constance.config.SLACK_PROBLEMS_CHANNEL_ID,blocks=blocks_public,text=f"A new Problem has been assigned to <@{self.assignee.slack_id}>! {self.problem} in {self.room}! The problem was reported by {self.name()}, he says its {URGENCY_DICT[self.urgency]}")
                else:
                    if self.urgency == 2:
                        public_message = client.chat_postMessage(channel=constance.config.SLACK_PROBLEMS_CHANNEL_ID,
                                                    text=f"<!channel> A new VERY URGENT Problem has been assigned to <@{self.assignee.slack_id}>! {self.problem} in {self.room}! The problem was reported by {self.name()}",
                                                    blocks=blocks_public)
                    else:
                        public_message = client.chat_postMessage(channel=constance.config.SLACK_PROBLEMS_CHANNEL_ID,blocks=blocks_public,text=f"A new Problem has been assigned to <@{self.assignee.slack_id}>! {self.problem} in {self.room}! The problem was reported by {self.name()}, he says its {URGENCY_DICT[self.urgency]}")
                    self.public_ts = public_message["message"]["ts"]

                private_message = client.chat_postMessage(channel=f"{self.assignee.slack_id}",
                                        text=f"A New problem has been assigned to you! {self.problem} in {self.room}! The problem was reported by {self.name()}, he says its {URGENCY_DICT[self.urgency]}",
                                        blocks=blocks_private)
                self.private_ts = private_message["message"]["ts"]
                self.private_id = private_message["channel"]

        except NameError:
            print("No client")

        super(problem, self).save(*args, **kwargs)


