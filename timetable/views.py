import json
import logging
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import model_to_dict
from django.views.decorators.http import require_GET
from . import forms
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import RegistrationForm, ClassForm, ScheduleForm
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.utils import timezone
from django.db.models import Q, Exists, OuterRef
from django.utils.translation import gettext_lazy as _

DAYS_OF_WEEKDAY = {
    6: 'Sunday',
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday'
}


def index(request):
    Subs = ClassNeedsSub.objects.filter(date=timezone.now().today())
    return render(request, 'index.html', {"Subs": Subs})


@login_required
def reportAbsence(request):
    form = forms.AbsenceForm()
    if request.method == 'POST':
        form = forms.AbsenceForm(request.POST)
        if form.is_valid():
            absence = Absence(teacher=request.user, date=form.cleaned_data['date'], reason=form.cleaned_data['reason'])
            absence.save()
            messages.success(request, _("Absence reported."))
            q = Class.objects.filter(teacher=request.user,
                                     day_of_week=DAYS_OF_WEEKDAY[form.cleaned_data['date'].weekday()])

            for c in q:
                newClass = ClassNeedsSub(Class_That_Needs_Sub=c, date=form.cleaned_data['date'])
                newClass.save()
            return HttpResponseRedirect(reverse('reportAbsence'))
        else:
            return HttpResponse("error")
    return render(request, "reportAbsence.html", {"form": form})


@permission_required('timetable.see_subs', login_url='/user/login/')
def sub(request):
    if request.method == 'POST':
        form = forms.SubstituteForm(request.POST)
        print(form.data)
        if form.is_valid():
            sub = form.cleaned_data['class_that_needs_sub']
            sub.substitute_teacher = Teacher.objects.filter(pk=form['substitute_teacher'].data).get()
            teacher = Teacher.objects.get(pk=form['substitute_teacher'].data)
            teacher.last_sub = form.cleaned_data['class_that_needs_sub'].date
            teacher.save()
            sub.save()


        else:
            print(form.errors)
    form = forms.SubstituteForm(initial={'substitute_teacher': "None selected"})
    return render(request, 'setSub.html', {"form": form,"ClassesThatNeedSub":ClassNeedsSub.objects.count()})


@login_required
def mySubs(request):
    mySubs = ClassNeedsSub.objects.filter(substitute_teacher=request.user).order_by('date')
    return render(request, "mySubs.html", {"mySubs": mySubs})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            teacher.save()
            return HttpResponseRedirect("/user/login/")
        else:
            return render(request, 'registration/register.html', {"form": form})
    form = forms.RegistrationForm()
    return render(request, 'registration/register.html', {"form": form})


@permission_required('timetable.see_classes')
def setClasses(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid:
            form.save()
        else:
            print(form.errors)
    form = forms.ClassForm
    classes = Class.objects.all()
    classesByHour = {}
    for c in classes:
        if (str(c.day_of_week) + "-" + str(c.hour)[:5]) not in classesByHour:
            classesByHour[str(c.day_of_week) + "-" + str(c.hour)[:5]] = 1
        else:
            classesByHour[str(c.day_of_week) + "-" + str(c.hour)[:5]] += 1
    return render(request, "setClasses.html", {"form": form, "classesByHour": classesByHour})


@require_GET
def get_possible_rooms(request):
    time = request.GET.get('hour')
    day = request.GET.get('day')
    rooms = Room.objects.filter(Exists(Class.objects.filter(room=OuterRef("pk"), hour=time, day_of_week=day)))
    availableRooms = []
    for room in rooms:
        availableRooms.append({'id': room.pk, 'name': room.name})
    return JsonResponse({"availableRooms": availableRooms})


@require_GET
def get_teacher_classes(request, n):
    classes = Class.objects.filter(teacher__pk=n)
    classesTimes = []
    for c in classes:
        classesTimes.append({'day': c.day_of_week, "hour": str(c.hour)[:5]})
    return JsonResponse({"classesTimes": classesTimes})


@require_GET
def get_possible_subs(request, n):
    c = ClassNeedsSub.objects.get(pk=n)
    filter_dict = {DAYS_OF_WEEKDAY[c.date.weekday()]: True}
    teacherQuery = Teacher.objects.filter(
        ~Exists(Class.objects.filter(teacher=OuterRef("pk"), day_of_week=DAYS_OF_WEEKDAY[c.date.weekday()],
                                     hour=c.Class_That_Needs_Sub.hour)),
        ~Exists(ClassNeedsSub.objects.filter(substitute_teacher=OuterRef("pk"), date=c.date,
                                             Class_That_Needs_Sub__hour=c.Class_That_Needs_Sub.hour)),
        ~Q(absence__date=c.date),
        can_substitute=True,
        **filter_dict)
    availableTeachers = []
    for teacher in teacherQuery:
        availableTeachers.append({'id': teacher.pk, 'name': teacher.username})
    return JsonResponse({"availableTeachers": availableTeachers})


def timetable(request):
    rooms = []
    for room in Room.objects.all():
        rooms.append(room.name)
    classes = Class.objects.all()
    teachers = []
    for t in Teacher.objects.all():
        teachers.append(t.username)
    classesByHour = {}
    for c in classes:
        grades = str(c.str_grades())
        grades_all = str(c.all_grades())
        if (str(c.day_of_week) + "-" + str(c.hour)[:5]) not in classesByHour:
            if c.teacher:
                classesByHour[str(c.day_of_week) + "-" + str(c.hour)[:5]] = [
                {"name":c.name, "all_grades":grades_all,"grades_display": grades,"teacher":c.teacher.username,"room":c.room.name}]
            else:
                classesByHour[str(c.day_of_week) + "-" + str(c.hour)[:5]] = [
                {"name":c.name,"all_grades":grades_all, "grades_display": grades,"teacher":c.student_teaching,"room":c.room.name}]
        else:
            if c.teacher:
                classesByHour[str(c.day_of_week) + "-" + str(c.hour)[:5]].append({"name":c.name, "grades_display": grades,"all_grades":grades_all,"teacher":c.teacher.username,"room":c.room.name})
            else:
                classesByHour[str(c.day_of_week) + "-" + str(c.hour)[:5]].append({"name":c.name, "grades_display": grades,"all_grades":grades_all,"teacher":c.student_teaching,"room":c.room.name})


    return render(request, "timetable.html", {"classesByHour": classesByHour,"teachers":teachers,"rooms":rooms})


def set_schedule(request,uuid):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return render(request, "thanks.html" )
    if Schedule.objects.filter(student__uuid=uuid).exists():
        return HttpResponse(_("A Schedule for This Student already Exists,Please Contact T.E.D!"))
    elif Student.objects.filter(uuid=uuid).exists():
        form = ScheduleForm({"student":uuid})
        return render(request,"set_schedule.html",{"form":form,"name":Student.objects.get(uuid=uuid).name})

    return HttpResponse(Http404)

def schedule_manager(request):
    students = []

    for student in Student.objects.all().order_by('schedule'):
        if Schedule.objects.filter(student__uuid=student.uuid).exists():
            students.append({student:True})
        else:
            students.append({student:False})
    print(students)
    return render(request,"schedule_manager.html",{"students":students})