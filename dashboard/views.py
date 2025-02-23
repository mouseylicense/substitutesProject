import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from dashboard.models import get_random_teacher
import timetable.models
from dashboard.models import problem
from .forms import ProblemForm, ProblemFormGuest
from collections import defaultdict

DAYS_OF_WEEKDAY_DICT = {
    6: 'Sunday',
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday'
}
# Create your views here.
def report(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ProblemForm(data=request.POST)
        else:
            form = ProblemFormGuest(data=request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return HttpResponseRedirect("thank_you")
    user = request.user
    if user.is_authenticated:
        return render(request,'report_form.html',{"form":ProblemForm(initial={"reporter": user})})
    else:
        return render(request,'report_form.html',{"form":ProblemFormGuest()})

def thank_you(request):
    return render(request,"thanks.html")

def dashboard(request):

    return render(request, 'dashboard.html',context={"rooms":timetable.models.Room.objects.filter(show_in_dashboard=True),"problems":problem.objects.all()})

def data(request):
    rooms = timetable.models.Room.objects.filter(show_in_dashboard=True)
    r = {}
    print(timezone.localtime(timezone.now()).strftime("%H:%m"))
    for room in rooms:
        if room.problem_set.count() == 0:
            r[room.name] = {"problems":""}
        else:
            r[room.name] = {"problems":list(room.problem_set.filter(resolved=False).values_list("problem", flat=True))}
        r[room.name]["isFree"] = room.get_class(timezone.localtime(timezone.now()).strftime("%H:%m"),DAYS_OF_WEEKDAY_DICT[timezone.now().weekday()])
    return JsonResponse(r)

@login_required
def stats(request):
    prob_by_teacher = defaultdict(lambda: {"resolved": 0, "not_resolved": 0})
    prob_by_assignee = defaultdict(lambda: {"resolved": 0, "not_resolved": 0})

    problems = problem.objects.all().order_by('date_reported')
    problems_resolved = problem.objects.filter(resolved=True)

    years = {year: [problem.objects.filter(date_reported__month=month, date_reported__year=year).count()
                    for month in [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]]
             for year in problem.objects.values_list('date_reported__year', flat=True).distinct()}

    for prob in problems:
        teacher_name = prob.name()
        assignee_name = prob.assignee.name()

        if prob.resolved:
            prob_by_teacher[teacher_name]["resolved"] += 1
            prob_by_assignee[assignee_name]["resolved"] += 1
        else:
            prob_by_teacher[teacher_name]["not_resolved"] += 1
            prob_by_assignee[assignee_name]["not_resolved"] += 1

    fixed_the_most = timetable.models.Teacher.objects.order_by('-resolved_problems').first()

    return render(request, 'dash_statistics.html', {
        "problems_by_teacher": json.dumps(prob_by_teacher),
        "problems_by_month": years,
        "problems_resolved": problems_resolved.count(),
        "total_problems": problems.count(),
        "fixed_the_most": fixed_the_most,
        "problems_by_assignee": json.dumps(prob_by_assignee)
    })


@login_required
def home(request):
    user = request.user
    myProblems = problem.objects.filter(assignee=user,resolved=False).order_by("-urgency")
    allProblems = problem.objects.filter(Q(resolved=False),~Q(assignee=user)).order_by("-urgency")
    return render(request,"dashboard_home.html",{"myProblems":myProblems,"allProblems":allProblems})


@login_required
@require_POST
def resolve(request):

    problem_id = request.POST['problem']
    prob = problem.objects.get(pk=problem_id)
    prob.resolve(request.user)
    return HttpResponse("OK")

@login_required()
@user_passes_test(lambda u: u.is_superuser or u.ted_manager)
def problems(request):
    return render(request,"problems.html",{"problems":problem.objects.filter(resolved=False).order_by("-urgency")})

@require_POST
@login_required
def change_assignee(request):
    problem_id = request.POST['problem']
    prob = problem.objects.get(pk=problem_id)
    prob.assignee = get_random_teacher()
    prob.save()
    res =  HttpResponse("OK")
    res["HX-Refresh"] = "true"

    return res