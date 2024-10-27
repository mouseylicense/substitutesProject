from datetime import datetime
from html.parser import HTMLParser

import django.template.defaultfilters
from bs4.builder import HTML_5
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import LaptopLoaningForm
from .models import LaptopPin
from django.conf import settings
from django.utils import timezone
# Create your views here.

def check_pin(request):
    pin = request.GET.get('pin')
    if LaptopPin.objects.filter(PIN=pin,granted=True).exists():

        pin = LaptopPin.objects.filter(PIN=pin).get()
        if pin.date == timezone.now().date():
            pin.use()
            return HttpResponse(200)
    return HttpResponseNotFound(404)

@login_required
def home(request):
    LaptopPin.objects.filter(date__lt=timezone.now()).delete()
    if request.method == 'POST':
        form = LaptopLoaningForm(request.POST)
        if form.is_valid():
            form.save()
    user = request.user
    return render(request,"laptops_home.html",{"form":LaptopLoaningForm(initial={"Teacher":user}),"grantedPins":LaptopPin.objects.filter(Teacher=user,granted=True).all().order_by("date").values(),"nonGrantedPins":LaptopPin.objects.filter(Teacher=user,granted=False).all().order_by("date").values()})

@login_required
def pin_manager(request):
    if request.method == 'POST':
        if request.POST.get('grant'):
            pin = LaptopPin.objects.get(id=int(request.POST.get('grant')))
            pin.grant()

            return render(request,'grantedPin.html',{"pin":pin})
        if request.POST.get('deny'):
            LaptopPin.objects.get(id=int(request.POST.get('deny'))).delete()
        return HttpResponse("test")

    return render(request,"laptops_pin_manager.html",{"pins":LaptopPin.objects.all()})
