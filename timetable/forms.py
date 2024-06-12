from _ast import Sub

from django import forms
from .models import *
from django.forms import DateInput,Select,TextInput

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = '__all__'

        widgets = {

            'teacher': Select(attrs={'class': 'form-select '}),
            'day': DateInput(attrs={'class': 'datepicker form-control','type':'date'}),
            'reason': TextInput(attrs={'class': 'form-control'}),
        }

