import copy
import json
from datetime import timedelta
import hmac
import hashlib
import constance
import slack_sdk
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import LaptopLoaning.models
import dashboard.models
import timetable.models
from django.conf import settings
client = slack_sdk.WebClient(token=settings.SLACK_BOT_TOKEN)
# Create your views here.
view = {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "Resolve Problems:"
            },
            "blocks": [

            ],
            "close": {
                "type": "plain_text",
                "text": "Close",
            },
            "callback_id": "problems_view"
        }
def verify_slack_request(request):

    slack_signing_secret = settings.SLACK_SIGNING_SECRET
    request_body = request.body.decode('utf-8')
    timestamp = request.META.get('HTTP_X_SLACK_REQUEST_TIMESTAMP',"")
    slack_signature = request.META.get('HTTP_X_SLACK_SIGNATURE',"")

    basestring = f"v0:{timestamp}:{request_body}".encode('utf-8')
    my_signature = 'v0=' + hmac.new(
        slack_signing_secret.encode('utf-8'),
        basestring,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(my_signature, slack_signature)
def problem_block(problem):
    return {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"{problem.problem} in {problem.room}, Reported by {problem.reporter}"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Resolve",
					"emoji": True
				},
                "style":"primary",
				"value":str(problem.id),
				"action_id": "resolve"
			}
		},



@csrf_exempt
def interactions(request):
    if not verify_slack_request(request):
        return HttpResponseForbidden("Invalid request signature")
    payload = json.loads(request.POST.get("payload","{}"))
    user = timetable.models.Teacher.objects.get(slack_id=payload["user"]['id'])
    print(payload)

    print(payload.get("type"))
    print(payload.keys())
    #Actions
    if payload.get("type") == "block_actions":
        action_id = payload['actions'][0]['action_id']
        if action_id == 'resolve':
            problem = dashboard.models.problem.objects.get(id=payload['actions'][0]['value'])
            problem.resolve(user)
            if "view" in payload:
                copy_of_view = copy.deepcopy(view)
                problems = user.assigned_problems.filter(resolved=False)
                if problems.count() == 0:
                    copy_of_view["blocks"] += {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "You have no assigned problems, Good job!"
                        }},
                else:
                    for problem in problems:
                        copy_of_view["blocks"] += problem_block(problem)
                client.views_update(trigger_id=payload["trigger_id"], view=copy_of_view, view_id=payload["view"]["id"])
        if action_id == 'grant':
            pin = LaptopLoaning.models.LaptopPin.objects.get(id=payload['actions'][0]['value'])
            pin.grant()
        if action_id == 'deny':
            pin = LaptopLoaning.models.LaptopPin.objects.get(id=payload['actions'][0]['value'])
            pin.deny()

    #Views
    if payload.get("type") == "view_submission":
        pass
    return JsonResponse({"response_action":"none"})

@require_POST
@csrf_exempt
def link_account(request):
    if not verify_slack_request(request):
        return HttpResponseForbidden("Invalid request signature")
    user = None
    for user in client.users_list()["members"]:
        if user["id"] == request.POST.get("user_id"):
            break
    user = timetable.models.Teacher.objects.get(email=user['profile']["email"])
    user.slack_id = request.POST.get("user_id")
    user.save()
    return HttpResponse("Successfully set id to " + user.slack_id)

@csrf_exempt
def fix_problems(request):
    if not verify_slack_request(request):
        return HttpResponseForbidden("Invalid request signature")
    copy_of_view = copy.deepcopy(view)

    user = timetable.models.Teacher.objects.get(slack_id=request.POST.get("user_id"))
    problems = user.assigned_problems.filter(resolved=False)
    if problems.count() == 0:
        copy_of_view["blocks"] += {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You have no assigned problems, Good job!"
            }},
    else:
        for problem in problems:
            copy_of_view["blocks"] += problem_block(problem)
    client.views_open(trigger_id=request.POST.get("trigger_id"),view=copy_of_view)
    return HttpResponse("")

@csrf_exempt
@require_GET
def door_open(request):
    pin = request.GET.get('pin')
    if LaptopLoaning.models.LaptopPin.objects.filter(PIN=pin,granted=True,expired=False).exists():
        pin = LaptopLoaning.models.LaptopPin.objects.filter(PIN=pin).get()
        client.chat_postMessage(channel=constance.config.SLACK_LAPTOPS_CHANNEL_ID,text=f"{pin.Teacher} left the door open")
    return HttpResponse("Door Opened")

@csrf_exempt
@require_POST
def otp(request):
    if not verify_slack_request(request):
        return HttpResponseForbidden("Invalid request signature")
    user = timetable.models.Teacher.objects.get(slack_id=request.POST.get("user_id"))
    pin = LaptopLoaning.models.LaptopPin(Teacher=user, date=timezone.now().date(), granted=True,
                                         expired=False, taking_time=timezone.now().time(),
                                         returning_time=timezone.now() + timedelta(minutes=5),
                                         room=timetable.models.Room.objects.first(), uses=1)
    pin.save()
    return HttpResponse(f"Your OTP is {pin.PIN}.")