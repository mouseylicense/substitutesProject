from _ast import Sub
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms import DateInput, Select, TextInput


class AbsenceForm(forms.Form):
        date = forms.DateField(widget=DateInput(attrs={'class': 'datepicker', 'type': 'date'}))
        reason = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-input','placeholder':'Reason'}))



# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = Teacher
#         fields = ["name", "password1", "password2", "phone_number", "email"]