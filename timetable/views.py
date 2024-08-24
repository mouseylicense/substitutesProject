import csv
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_POST
from SubtitutesProject.settings import BASE_DIR
from . import forms
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import RegistrationForm, ClassForm, ScheduleForm, TeacherForm, SuperuserCreationForm, \
    StudentRegistrationForm, DescriptionChangeForm
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404 ,FileResponse
from django.utils import timezone
from django.db.models import Q, Exists, OuterRef
from django.utils.translation import gettext_lazy as _
import datetime
from dotenv import load_dotenv
from os import environ
from constance import config

load_dotenv()
FROM_EMAIL=environ['FROM_EMAIL']
HOUR_TO_NUMBER_OF_CLASS = {
    datetime.time(9,15):"first",
    datetime.time(10,7):"second",
    datetime.time(11,45):"third",
    datetime.time(12,45):"fourth",
}
DAYS_OF_WEEKDAY = {
    6: 'Sunday',
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday'
}
HEBREW_GRADES_TO_GRADES= {
    'א':0,
    'ב':1,
    'ג':2,
    'ד':3,
    'ה':4,
    'ו':5,
    'ז':6,
    'ח':7,
    'ט':8,
    'י':9,
    'יא':10,
    'יב':11,
}

def importCsv(path):
    with open(path,encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            _,created = Student.objects.get_or_create(
                name=row[1] + " " + row[0],
                grade=HEBREW_GRADES_TO_GRADES[row[4]]

            )

def index(request):
    if not Teacher.objects.exists():
        if request.method == 'POST':
            form = SuperuserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                return form.errors
        return render(request, 'first_time.html',{"form":SuperuserCreationForm})
    Subs = ClassNeedsSub.objects.filter(date=timezone.now().today())
    return render(request, 'index.html', {"Subs": Subs})

@login_required()
@user_passes_test(lambda u: u.manage_subs or u.is_superuser)
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
    return render(request, 'setSub.html', {"form": form, "ClassesThatNeedSub": ClassNeedsSub.objects.count()})

@login_required()
def teacher_home(request):
    if request.method == 'POST':
        form = forms.AbsenceForm(request.POST)
        if form.is_valid():
            if not Absence.objects.filter(teacher=request.user, date=form.cleaned_data['date']).exists():
                absence = Absence(teacher=request.user, date=form.cleaned_data['date'],
                                  reason=form.cleaned_data['reason'])
                absence.save()
                messages.success(request, _("Absence reported."))
                q = Class.objects.filter(teacher=request.user,
                                         day_of_week=DAYS_OF_WEEKDAY[form.cleaned_data['date'].weekday()])

                for c in q:
                    newClass = ClassNeedsSub(Class_That_Needs_Sub=c, date=form.cleaned_data['date'])
                    newClass.save()
            else:
                messages.error(request, _("Absence already reported."))
        else:
            return HttpResponse("error")
    Absence.objects.filter(date__lt=timezone.now().date()).delete()
    form = forms.AbsenceForm()
    mySubs = ClassNeedsSub.objects.filter(substitute_teacher=request.user).order_by('date').values("Class_That_Needs_Sub__room","Class_That_Needs_Sub__name","date","Class_That_Needs_Sub__hour")
    myAbsences = Absence.objects.filter(teacher=request.user).order_by('date').values("date","reason")
    return render(request, "teacher_home.html", {"mySubs": mySubs,"form":form,"myAbsence":myAbsences})

def register(request,uuid):
    if request.method == 'POST':
        form = RegistrationForm(request.POST,instance=Teacher.objects.get(uuid=uuid))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login"))
        else:
            return render(request, 'registration/register.html', {"form": form})
    form = forms.RegistrationForm(instance=Teacher.objects.get(uuid=uuid))
    return render(request, 'registration/register.html', {"form": form})

@login_required()
@user_passes_test(lambda u: u.manage_schedule or u.is_superuser)
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
        **filter_dict).values("pk","first_name")
    availableTeachers = []
    for teacher in teacherQuery:
        print(teacher)
        availableTeachers.append({'id': teacher['pk'], 'name': teacher['first_name']})
    return JsonResponse({"availableTeachers": availableTeachers})


def timetable(request):
    rooms = []
    for room in Room.objects.all():
        rooms.append(room.name)
    classes = Class.objects.all()
    teachers = []
    for t in Teacher.objects.all():
        teachers.append(t.first_name)
    classesByHour = {}
    for c in classes:
        grades = str(c.str_grades())
        grades_all = str(c.all_grades())
        if (str(c.day_of_week) + "-" + str(c.hour)[:5]) not in classesByHour:
            if c.teacher:
                classesByHour[str(c.day_of_week) + "-" + str(c.hour)[:5]] = [
                    {"name": c.name, "all_grades": grades_all, "grades_display": grades, "teacher": c.teacher.first_name,
                     "room": c.room.name,"description":c.description}]
            else:
                classesByHour[str(c.day_of_week) + "-" + str(c.hour)[:5]] = [
                    {"name": c.name, "all_grades": grades_all, "grades_display": grades, "teacher": c.student_teaching,
                     "room": c.room.name,"description":c.description}]
        else:
            if c.teacher:
                classesByHour[str(c.day_of_week) + "-" + str(c.hour)[:5]].append(
                    {"name": c.name, "grades_display": grades, "all_grades": grades_all, "teacher": c.teacher.first_name,
                     "room": c.room.name,"description":c.description})
            else:
                classesByHour[str(c.day_of_week) + "-" + str(c.hour)[:5]].append(
                    {"name": c.name, "grades_display": grades, "all_grades": grades_all, "teacher": c.student_teaching,
                     "room": c.room.name,"description":c.description})

    return render(request, "timetable.html", {"classesByHour": classesByHour, "teachers": teachers, "rooms": rooms})


def set_schedule(request, uuid):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return render(request, "thanks.html")
    if Schedule.objects.filter(student__uuid=uuid).exists():
        return HttpResponse(_("A Schedule for This Student already Exists,Please Contact T.E.D!"))
    elif Student.objects.filter(uuid=uuid).exists():
        form = ScheduleForm({"student": uuid})
        return render(request, "set_schedule.html", {"form": form, "name": Student.objects.get(uuid=uuid).name})

    return Http404


def student_details(request,uuid):
    student = Student.objects.get(uuid=uuid)
    res = render(request, "student_details.html", {"student": student})
    res["HX-Trigger"] = "unfold"
    return res
@login_required()
@user_passes_test(lambda u: u.is_superuser)
def teacher_manager(request):
    if request.method == "POST":
        if request.body.decode("utf-8").split("=")[0] == "Delete":
            Teacher.objects.get(uuid=request.body.decode("utf-8").split("=")[1]).delete()
            return HttpResponse("")
        else:
            form = TeacherForm(request.POST)
            form.instance = Teacher.objects.get(uuid=form["uuid"].value())
            if form.is_valid():
                form.save()
            else:
                return HttpResponse(form.errors)
    teachers = Teacher.objects.all()
    teachers_and_forms = {}
    for teacher in teachers:
        teachers_and_forms[teacher] = TeacherForm(instance=teacher,initial={"uuid":teacher.uuid})
    return render(request, "teacher_manager.html", {"teachers": teachers_and_forms})

@login_required
def student_manager(request):
    if request.method == "POST":
        print(request.POST)
        payload = request.POST.get("userCreation")
        if payload == "on":
            config.ADDING_STUDENTS = True

        if payload is None:
            config.ADDING_STUDENTS = False
    user = request.user
    if user.is_superuser:
        student_pool = Student.objects.all()
        scheduleCount = Schedule.objects.count()
        studentWithNoSchedule = Student.objects.count()-Schedule.objects.count()
    else:
        student_pool = Student.objects.filter(tutor=user)
        scheduleCount = Schedule.objects.filter(student__tutor=user).count()
        studentWithNoSchedule = Student.objects.filter(tutor=user).count()-Schedule.objects.filter(student__tutor=user).count()
    students = {}
    for student in student_pool:
        students[student.name] = [student.uuid,Schedule.objects.filter(student=student).exists(),datetime.datetime.strftime(timezone.localtime(student.last_schedule_invite), '%d/%m/%Y %H:%M')]
    return render(request,"student_manager.html",{"students":students,"scheduleCount":scheduleCount,
                                                     "studentWithNoSchedule":studentWithNoSchedule,"creationEnabled":config.ADDING_STUDENTS})

@require_POST
@login_required
def send_email(request):
    if request.is_secure():
        method = "https://"
    else:
        method = "http://"
    if request.method == "POST":
        payload = request.body.decode("utf-8").split("=")
        res = HttpResponse(status=200)
        res["HX-Refresh"] = "true"
        if payload[1] == "reset-all":
            Schedule.objects.all().delete()

            return res

        elif payload[1] == "invite-all":
            students = Student.objects.all().exclude(schedule__isnull=False)
            for student in students:
                send_mail(
                    "Set Schedule Invite!",
                    f'Hello {student.name},please Set your school schedule in the following link {request.get_host()}{reverse(set_schedule,args=[student.uuid])}',
                    FROM_EMAIL,
                    [student.email],
                    html_message=render_to_string("emails/setSchedule_email.html", {"student": student.name,
                                                                               "link": method + request.get_host() + reverse(
                                                                                   set_schedule, args=[student.uuid])}),
                    fail_silently=False,
                )
                student.last_schedule_invite = timezone.now()
                student.save()
            return res


        else:
            student = Student.objects.get(uuid=payload[0])
            student.last_schedule_invite = timezone.now()
            student.save()
            if payload[1] == "True":

                student.schedule.delete()
                send_mail(
                    "Schedule Reset",
                    f'Hello {student.name},Your Schedule has been reset, please set it again at the following link: {request.get_host()}{reverse(set_schedule, args=[student.uuid])}',
                    FROM_EMAIL,
                    html_message=render_to_string("emails/setScheduleReset_email.html", {"student": student.name,
                                                                                    "link": method + request.get_host() + reverse(
                                                                                        set_schedule,
                                                                                        args=[student.uuid])}),
                    recipient_list=[student.email],
                    fail_silently=False,
                )
                return res
            else:
                send_mail(
                    "Set Schedule Invite!",
                    f'Hello {student.name},please Set your school schedule in the following link {request.get_host()}{reverse(set_schedule,args=[student.uuid])}',
                    FROM_EMAIL,
                    [student.email],
                    html_message=render_to_string("emails/setSchedule_email.html", {"student": student.name,
                                                                               "link": method + request.get_host() + reverse(
                                                                                   set_schedule, args=[student.uuid])}),

                    fail_silently=False,
                )
                test = HttpResponse(datetime.datetime.strftime(timezone.localtime(student.last_schedule_invite), '%d/%m/%Y %H:%M'))
                test["HX-Trigger"] = "alert"
                return test

def printable(request):
    day = DAYS_OF_WEEKDAY[timezone.now().weekday()]
    classes = Class.objects.filter(day_of_week=day).order_by('hour').all()
    classes_by_hour = {}
    for c in classes:
        if classes_by_hour.get(str(c.hour)[:5]):
            classes_by_hour[str(c.hour)[:5]].append(c)
        else:
            if str(c.hour)[:5] == "11:45":
                classes_by_hour["11:00"] = []
            classes_by_hour[str(c.hour)[:5]] = [c]
    return render(request,"day_schedule.html",{"day":_(day),"classes":classes_by_hour})
@require_POST
@login_required()
@user_passes_test(lambda u: u.is_superuser)
def create_teacher(request):
    if request.is_secure():
        method = "https://"
    else:
        method = "http://"
    email = request.headers["HX-Prompt"]
    try:
        validate_email(email)
    except ValidationError as e:
        return HttpResponse(str(e))
    else:
        if not Teacher.objects.filter(email=email).exists():
            teacher = Teacher(email=email)
            teacher.save()
        else:
            teacher = Teacher.objects.get(email=email)

        url = method + request.get_host() + reverse("register", args=[teacher.uuid])
        return HttpResponse(url)

@require_POST
@login_required()
def delete_absence(request):
    payload = request.body.decode("utf-8").split("=")
    if Absence.objects.filter(teacher__uuid=payload[0],date=payload[1]).exists():
        Absence.objects.filter(teacher__uuid=payload[0],date=payload[1]).delete()
        return HttpResponse(200)
    return HttpResponse(404)

@login_required()
@user_passes_test(lambda u: u.is_superuser)
def danger_zone(request):
    if request.method == "POST":
        payload = request.body.decode("utf-8").split("=")
        print(payload)
        if payload[2] == 'delete-schedules':
            Schedule.objects.all().delete()
        if payload[2] == 'increase-grades':
            for s in Student.objects.all():
                s.increment_grade()
        if payload[2] == 'delete-tutors':
            for s in Student.objects.all():
                s.tutor = None
                s.save()
        if payload[2] == 'delete-classes':
            Class.objects.all().delete()
        if payload[2] == 'delete-shachariot':
            for s in Student.objects.all():
                s.shachariot = None
                s.save()

    return render(request,"dangerzone.html")


def register_student(request,):
    if config.ADDING_STUDENTS:
        if request.method == "POST":
            form = StudentRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        form = StudentRegistrationForm()
        return render(request,"studentregister.html",{"form":form})
    return HttpResponse("Registering Students is currently disabled")

def class_manager(request):
    classes_and_students = {}
    for c in Class.objects.all():
        classes_and_students[c.name] = Schedule.objects.filter(**{c.day_of_week.lower() +"_"+ HOUR_TO_NUMBER_OF_CLASS[c.hour]:c}).count()
    form = DescriptionChangeForm()

    return render(request,"class_manager.html",{"classes":classes_and_students,"DescriptionForm":form})

