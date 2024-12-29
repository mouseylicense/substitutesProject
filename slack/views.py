import copy
import json

import slack_sdk
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
def resolve_problem(request):

    payload = json.loads(request.POST.get("payload"))
    user = timetable.models.Teacher.objects.get(slack_id=payload["user"]['id'])


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
        client.views_update(trigger_id=payload["trigger_id"], view=copy_of_view,view_id=payload["view"]["id"])
    return HttpResponse("test")

@require_POST
@csrf_exempt
def link_account(request):
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