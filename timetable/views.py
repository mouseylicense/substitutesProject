import logging
from . import forms
from django.contrib import messages
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
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

#return teachers avaiable at certain day
def absences(request):
    classes = Class.objects.filter(needs_sub=True)
    if classes.exists():
        return HttpResponse(Teacher.objects.filter(~Q(absence__day=str(classes)),~Q(class__hour=classes.get().hour)),)
    else:
        return HttpResponse("no abscence")
def reportAbsence(request):
    form = forms.AbsenceForm()
    if request.method == 'POST':
        form = forms.AbsenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Absence reported.")
            q = Class.objects.filter(teacher=form.cleaned_data['teacher'],day_of_week=DAYS_OF_WEEKDAY[form.cleaned_data['day'].weekday()])
            for c in q:
                c.needs_sub = True
                c.save()
            return HttpResponseRedirect(reverse('report'))
        else:
            return HttpResponse("error")
    return render(request,"reportAbsence.html", {"form": form})

#set sub
def sub(request):
    return render(request,'setSub.html',{"classes":Class.objects.filter(needs_sub=True).order_by("day_of_week", "hour")})

