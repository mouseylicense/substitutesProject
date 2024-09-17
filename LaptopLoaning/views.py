from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .forms import LaptopLoaningForm
from .models import LaptopPin

# Create your views here.

def check_pin(request):
    pin = request.GET.get('pin')
    if LaptopPin.objects.filter(PIN=pin,granted=True).exists():

        pin = LaptopPin.objects.filter(PIN=pin).get()
        if pin.date == datetime.today().date():
            pin.use()
            return HttpResponse(200)
    return HttpResponseNotFound(404)

@login_required
def laptops_home(request):
    if request.method == 'POST':
        form = LaptopLoaningForm(request.POST)
        if form.is_valid():
            form.save()
    user = request.user
    return render(request,"order_laptops.html",{"form":LaptopLoaningForm(initial={"Teacher":user}),"grantedPins":LaptopPin.objects.filter(Teacher=user,granted=True).all().order_by("date").values(),"nonGrantedPins":LaptopPin.objects.filter(Teacher=user,granted=False).all().order_by("date").values()})