import logging

from django.contrib.auth.decorators import login_required, permission_required
from django.forms import model_to_dict
from django.views.decorators.http import require_GET

from . import forms
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import RegistrationForm
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

@permission_required('timetable.add_classneedssub',login_url='/user/login/')
def sub(request):
    if request.method == 'POST':
        form = forms.SubstituteForm(request.POST)
        print(form.data)
        if form.is_valid():
            sub = form.cleaned_data['class_that_needs_sub']
            sub.substitute_teacher = Teacher.objects.filter(pk=form['substitute_teacher'].data).get()
            sub.save()


        else:
            print(form.errors)
    form = forms.SubstituteForm(initial={'substitute_teacher':"None selected"})
    return render(request, 'setSub.html', {"form": form})

@require_GET
def get_possible_subs(request,n):
    c = ClassNeedsSub.objects.get(pk=n)
    teacherQuery = Teacher.objects.filter(~Q(absence__date=str(c.date)),~Q(class__hour=c.Class_That_Needs_Sub.hour)).order_by('last_sub')
    availableTeachers = []
    for teacher in teacherQuery:
        availableTeachers.append({'id':teacher.pk, 'name':teacher.name})
    return JsonResponse({"availableTeachers": availableTeachers})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            teacher.save()
            return HttpResponseRedirect("/user/login/")
        else:
            return render(request,'registration/register.html',{"form":form})
    form = forms.RegistrationForm()
    return render(request,'registration/register.html',{"form":form})