import logging

from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q

# Create your views here.

DAYS_OF_WEEKDAY = {
    6: 'Sunday',
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday'
}
def index(request):
    classes_by_day = {"Sunday": [], "Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": []}
    for i in classes_by_day:
        classes_by_day[i] = Class.objects.filter(day_of_week=i).order_by("hour")
    return render(request, 'index.html',
                  {"classes": classes_by_day, "teacher": Teacher.objects.all().order_by("last_sub")})


def retrieve_classes(request, teacher):
    return HttpResponse(Class.objects.filter(teacher__name=teacher).order_by("day_of_week", "hour").__dir__)



def absences(request):
    oneabsence = Absence.objects.get()
    classes = Class.objects.filter(teacher=oneabsence.teacher,day_of_week=DAYS_OF_WEEKDAY[oneabsence.day.weekday()])
    return HttpResponse(Teacher.objects.filter(~Q(abscence__day=str(timezone.now().date())),class__hour=classes.get().hour))
    # return HttpResponse(classes)




