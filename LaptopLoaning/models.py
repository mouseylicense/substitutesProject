import datetime
from random import randint
import constance
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from slack_sdk import WebClient

import timetable.models

if hasattr(settings, 'SLACK_BOT_TOKEN'):


    client = WebClient(token=settings.SLACK_BOT_TOKEN)
def generate_pin():
    return ''.join(str(randint(0, 9)) for _ in range(4))


# Create your models here.
class LaptopPin(models.Model):
    Teacher = models.ForeignKey(timetable.models.Teacher, on_delete=models.CASCADE)
    PIN = models.CharField(max_length=4, default=generate_pin, unique=True)
    reason = models.CharField(max_length=255, default='')
    date = models.DateField()
    taking_time = models.TimeField()
    returning_time = models.TimeField()
    room = models.ForeignKey(timetable.models.Room, on_delete=models.CASCADE)
    uses = models.IntegerField(default=2)
    numberOfLaptops = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    granted = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    slack_ts = models.CharField(max_length=255, default='', blank=True)
    def use(self):
        self.uses = self.uses - 1
        if self.uses <= 0:
            self.expired = True
            self.save()
        else:
            self.save()
        try:
            client.chat_postMessage(channel=constance.config.SLACK_LAPTOPS_CHANNEL_ID, text=f"{self.Teacher} used PIN {self.PIN} for {self.reason} in room {self.room} \n This PIN now has {self.uses} uses left")
        except Exception as e:
            print(e)
            print("Slack not configured")
    def __str__(self):
        return f"{self.Teacher} - {self.PIN} - {self.date}"
    def save(self, *args, **kwargs):
        if not self.pk:
                if self.granted == False:
                    super().save(*args, **kwargs)
                    try:

                        GRANT_BLOCK = [
                            {
                                "text": {
                                    "text": f"{self.Teacher} requested {self.numberOfLaptops} Laptops for {self.reason} in room {self.room} \n From {self.taking_time} to {self.returning_time} on {self.date}",
                                    "type": "mrkdwn"
                                },
                                "type": "section"
                            }, {
                                "type": "actions",
                                "block_id": "grant",
                                "elements": [{
                                    "type": "button",
                                    "style": "primary",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Grant",
                                    },
                                    "value": f"{self.id}",
                                    "action_id": "grant"
                                },{
                                    "type": "button",
                                    "style": "danger",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Deny",
                                    },
                                    "value": f"{self.id}",
                                    "action_id": "deny"
                                }]}
                        ]
                        message = client.chat_postMessage(channel=constance.config.SLACK_LAPTOPS_CHANNEL_ID,blocks=GRANT_BLOCK, text=GRANT_BLOCK[0]['text']['text'])
                        self.slack_ts = message['ts']
                    except Exception as e:
                        print(e)
                        print("Slack not configured")
        super().save(*args, **kwargs)
    def grant(self):
        self.granted = True
        self.save()
        try:
            client.chat_update(channel=constance.config.SLACK_LAPTOPS_CHANNEL_ID,ts=self.slack_ts,text=f" ~{self.Teacher} requested {self.numberOfLaptops} Laptops for {self.reason} in room {self.room}~ \n ~From {self.taking_time} to {self.returning_time} on {self.date}~ \n *Granted,Code is {self.PIN}*")
        except Exception as e:
            print(e)
            print("Slack not configured")
    def deny(self):
        self.expired = True
        self.granted = False
        self.save()
        try:
            client.chat_update(channel=constance.config.SLACK_LAPTOPS_CHANNEL_ID,ts=self.slack_ts,text=f" ~{self.Teacher} requested {self.numberOfLaptops} Laptops for {self.reason} in room {self.room}~ \n ~From {self.taking_time} to {self.returning_time} on {self.date}~ \n *Denied*")
        except Exception as e:
            print(e)
            print("Slack not configured")