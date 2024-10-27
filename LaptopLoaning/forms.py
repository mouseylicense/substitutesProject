from django import forms
from .models import LaptopPin
from django.utils.translation import gettext_lazy as _

class LaptopLoaningForm(forms.ModelForm):
    class Meta:
        model = LaptopPin
        fields = ("Teacher","date","numberOfLaptops","room")
        labels = {
            "Teacher" : _("Teacher"),
            "date" : _("Date"),
            "numberOfLaptops" : _("Number Of Laptops"),
            "room" : _("Room")
        }
        widgets = {
            "Teacher":forms.HiddenInput(),
            "date": forms.DateInput(attrs={'type': 'date'})
        }