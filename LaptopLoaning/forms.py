from constance import config
from django import forms
from .models import LaptopPin
from django.utils.translation import gettext_lazy as _

class LaptopLoaningForm(forms.ModelForm):
    class Meta:
        model = LaptopPin
        fields = ("Teacher","reason","date","numberOfLaptops","room","taking_time","returning_time")
        labels = {
            "Teacher" : _("Teacher"),
            "reason" : _("For?"),
            "date" : _("Date"),
            "numberOfLaptops" : _("Number Of Laptops"),
            "room" : _("Room"),
            "taking_time" : _("From"),
            "returning_time" : _("Until"),
        }
        widgets = {
            "reason": forms.TextInput(attrs={'placeholder': _("Reason")}),
            "Teacher":forms.HiddenInput(),
            "date": forms.DateInput(attrs={'type': 'date'}),
            "numberOfLaptops":forms.NumberInput(attrs={'id':'numberOfLaptops','type': 'range','min':1}),
            "taking_time": forms.TimeInput(attrs={'type':'time','onChange':'setMin(this)'}),
            "returning_time": forms.TimeInput(attrs={'type':'time','id':'returning_time'},format='%H:%M'),
        }
