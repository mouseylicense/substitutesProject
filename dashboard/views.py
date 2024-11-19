import json

from django.shortcuts import render

import timetable.models
from dashboard.models import problem
from .forms import ProblemForm
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


def test(request):
    return render(request, 'edit.html',context={"rooms":timetable.models.Room.objects.all(),"problems":problem.objects.all()})


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
                prob_by_teacher[prob.reporter.name()] = {"resolbed": 1, "not_resolved": 0}
            else:
                prob_by_teacher[prob.reporter.name()] = {"resolved": 0, "not_resovled": 1}

    return render(request, 'statistics.html',
                  {"pins_by_teacher": json.dumps(prob_by_teacher), "pins_by_month": years,
                   "pins_granted": problems_resolved.count(), "total_laptops": problems.count()})