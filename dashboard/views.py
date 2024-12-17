import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST
from dashboard.models import get_random_teacher
import timetable.models
from dashboard.models import problem
from .forms import ProblemForm

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
        form = ProblemForm(data=request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return render(request,"thanks.html")
    user = request.user
    return render(request,'report_form.html',{"form":ProblemForm(initial={"reporter": user})})


def dashboard(request):

    return render(request, 'dashboard.html',context={"rooms":timetable.models.Room.objects.all(),"problems":problem.objects.all()})

def data(request):
    rooms = timetable.models.Room.objects.all()
    r = {}
    print(timezone.localtime(timezone.now()).strftime("%H:%m"))
    for room in rooms:
        if room.problem_set.count() == 0:
            r[room.name] = {"problems":""}
        else:
            r[room.name] = {"problems":list(room.problem_set.filter(resolved=False).values_list("problem", flat=True))}
        r[room.name]["isFree"] = room.get_class(timezone.localtime(timezone.now()).strftime("%H:%m"),DAYS_OF_WEEKDAY_DICT[timezone.now().weekday()])
    return JsonResponse(r)

def stats(request):
    prob_by_teacher = {}
    problems = problem.objects.all().order_by('date_reported')
    problems_resolved = problem.objects.filter(resolved=True)
    years = {}
    for k in problem.objects.all().values_list('date_reported__year'):
        if k[0] not in years:
            years[k[0]] = []
    for year in years:
        for month in [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]:
            years[year].append(problem.objects.filter(date_reported__month=month, date_reported__year=year).count())
    for prob in problems:
        try:
            if prob.resolved:
                prob_by_teacher[prob.reporter.name()]['resolved'] += 1
            else:
                prob_by_teacher[prob.reporter.name()]['not_resolved'] += 1
        except KeyError:
            if prob.resolved:
                prob_by_teacher[prob.reporter.name()] = {"resolved": 1, "not_resolved": 0}
            else:
                prob_by_teacher[prob.reporter.name()] = {"resolved": 0, "not_resolved": 1}
    fixed_the_most = timetable.models.Teacher.objects.order_by('-resolved_problems').first()
    return render(request, 'dash_statistics.html',
                  {"problems_by_teacher": json.dumps(prob_by_teacher), "problems_by_month": years,
                   "problems_resolved": problems_resolved.count(), "total_problems": problems.count(),"fixed_the_most": fixed_the_most})
@login_required
def home(request):
    user = request.user
    myProblems = problem.objects.filter(assignee=user,resolved=False).order_by("-urgency")
    return render(request,"dashboard_home.html",{"myProblems":myProblems})


@login_required
@require_POST
def resolve(request):

    problem_id = request.POST['problem']
    prob = problem.objects.get(pk=problem_id)
    prob.resolved = True
    prob.resolved_by = request.user
    prob.save()
    return HttpResponse("OK")

@login_required()
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