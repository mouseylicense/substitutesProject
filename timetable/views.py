import logging

from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from . import forms
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.db.models import Q

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


@login_required
def reportAbsence(request):
    form = forms.AbsenceForm()
    if request.method == 'POST':
        form = forms.AbsenceForm(request.POST)
        if form.is_valid():
            absence = Absence(teacher=request.user,date=form.cleaned_data['date'],reason=form.cleaned_data['reason'])
            absence.save()
            messages.success(request, "Absence reported.")
            q = Class.objects.filter(teacher=request.user,
                                     day_of_week=DAYS_OF_WEEKDAY[form.cleaned_data['date'].weekday()])

            for c in q:
                newClass = ClassNeedsSub(Class_That_Needs_Sub=c, date=form.cleaned_data['date'])
                newClass.save()
            return HttpResponseRedirect(reverse('report'))
        else:
            return HttpResponse("error")
    return render(request, "reportAbsence.html", {"form": form})


def sub(request):
    print(ClassNeedsSub.objects.all())
    return render(request, 'setSub.html', {"classes": ClassNeedsSub.objects.all().order_by("date")})


def get_possible_subs(request,n):
    c = ClassNeedsSub.objects.get(pk=n)
    teacherQuery = Teacher.objects.filter(~Q(absence__date=str(c.date)),~Q(class__hour=c.Class_That_Needs_Sub.hour)).order_by('last_sub')
    availableTeachers = []
    for teacher in teacherQuery:
        availableTeachers.append(model_to_dict(teacher))
    return JsonResponse({"availableTeachers": availableTeachers})
