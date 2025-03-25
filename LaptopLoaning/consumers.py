# chat/consumers.py
import json

from django.utils import timezone

from .models import *
from channels.generic.websocket import WebsocketConsumer

if hasattr(settings, 'SLACK_BOT_TOKEN'):
    client = WebClient(token=settings.SLACK_BOT_TOKEN)


class PinConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close()
    def receive(self, text_data):

        print(text_data)
        pin = text_data[-4:]
        pinObject = LaptopPin.objects.filter(PIN=pin, granted=True, expired=False,date=timezone.now().date()).first()
        if len(text_data)==10:
            print("closed")
        elif len(text_data)==9:
            if pinObject is not None:
                print(f"{pinObject.Teacher} left the door open")
                try:
                    client.chat_postMessage(channel=constance.config.SLACK_LAPTOPS_CHANNEL_ID,
                                        text=f"{pinObject.Teacher} left the door open")
                except Exception as e:
                    print(e)
                    print("Slack not configured")
        elif len(text_data) == 7 :
            if pinObject is not None:
                pinObject.use()
        else:
            if pinObject is not None:
                self.send(text_data="True")
            else:

                self.send(text_data="False")

