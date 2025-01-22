import json
from dataclasses import fields
from datetime import datetime

from constance import config
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .forms import LaptopLoaningForm
from .models import LaptopPin
from django.utils import timezone
# Create your views here.

@require_GET
def check_pin(request):
    pin = request.GET.get('pin')
    if LaptopPin.objects.filter(PIN=pin,granted=True,expired=False).exists():

        pin = LaptopPin.objects.filter(PIN=pin).get()
        if pin.date == timezone.now().date():
            pin.use()
            return HttpResponse(200)
    return HttpResponseNotFound(503)

@login_required
def home(request):
    LaptopPin.objects.filter(date__lt=timezone.now()).expire = True
    if request.method == 'POST':
        form = LaptopLoaningForm(request.POST)
        if form.is_valid():
            form.save()
    user = request.user
    return render(request,"laptops_home.html",{"form":LaptopLoaningForm(initial={"Teacher":user}),"maxLaptops":config.LAPTOPS,"grantedPins":LaptopPin.objects.filter(Teacher=user,granted=True, expired=False).all().order_by("date").values(),"nonGrantedPins":LaptopPin.objects.filter(Teacher=user,granted=False,expired=False).all().order_by("date").values()})

@user_passes_test(lambda u: u.is_superuser or u.type == 1 or u.manage_ted)
@login_required
def pin_manager(request):
    if request.method == 'POST':
        if request.POST.get('grant'):
            pin = LaptopPin.objects.get(id=int(request.POST.get('grant')))
            pin.grant()

            return render(request,'grantedPin.html',{"pin":pin})
        if request.POST.get('deny'):
            pin = LaptopPin.objects.get(id=int(request.POST.get('deny')))
            pin.expired = True
            pin.granted = False
            pin.save()
        return HttpResponse("test")

    return render(request,"laptops_pin_manager.html",{"pins":LaptopPin.objects.filter(expired=False)})

# TODO: make this actually work , this is not a good way to figure out how many laptops are available for the entire session,
#  this needs to be thought out more
@require_GET
@login_required
def returnAvailable(request):
    day,month,year = int(request.GET.get('day')),int(request.GET.get('month')),int(request.GET.get('year'))
    hour = int(request.GET.get('hour'))
    minute = int(request.GET.get('minute'))
    occupied = 0
    for i in LaptopPin.objects.filter(granted=True,date=timezone.datetime(day=day,month=month,year=year),taking_time__lt=f"{hour}:{minute}:00",returning_time__gt=f"{hour}:{minute}:00"):
        occupied += i.numberOfLaptops
    available = config.LAPTOPS - occupied
    return HttpResponse(available)

@user_passes_test(lambda u: u.is_superuser or u.type == 1 or u.manage_ted)
@login_required()
def stats(request):
    pins_by_teacher = {}
    pins = LaptopPin.objects.all().order_by('date')
    pins_granted = LaptopPin.objects.filter(granted=True)
    total_laptops = 0
    years = {}
    time_used = timezone.timedelta()
    for i in pins_granted:
        total_laptops += i.numberOfLaptops
        time_used += datetime.combine(timezone.datetime.today(), i.returning_time) - datetime.combine(timezone.datetime.today(), i.taking_time)
    for k in LaptopPin.objects.all().values_list('date__year'):
        if k[0] not in years:
            years[k[0]] = []
    for year in years:
        for month in [9,10,11,12,1,2,3,4,5,6]:
            years[year].append(LaptopPin.objects.filter(date__month=month,date__year=year).count())
    for pin in pins:
        try:
            if pin.granted:
                pins_by_teacher[pin.Teacher.name()]['granted'] += 1
            else:
                pins_by_teacher[pin.Teacher.name()]['not_granted'] += 1
        except KeyError:
            if pin.granted:
                pins_by_teacher[pin.Teacher.name()] = {"granted":1,"not_granted":0}
            else:
                pins_by_teacher[pin.Teacher.name()] = {"granted":0,"not_granted":1}

    return render(request,'statistics.html',{"pins_by_teacher":json.dumps(pins_by_teacher),"pins_by_month":years,"total_time":time_used,"pins_granted":pins_granted.count(),"total_laptops":total_laptops})