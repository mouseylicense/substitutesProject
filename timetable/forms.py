from _ast import Sub

from django import forms
from .models import *
from django.forms import DateInput, Select, TextInput


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = '__all__'

        widgets = {

            'teacher': Select(attrs={'class': 'select'}),
            'date': DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
            'reason': TextInput(attrs={'class': 'text-input'}),
        }
