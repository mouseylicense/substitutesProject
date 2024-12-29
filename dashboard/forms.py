from django import forms
from dashboard.models import *
from django.forms import DateInput, Select, TextInput, HiddenInput, PasswordInput
from django.utils.translation import gettext_lazy as _
class ProblemForm(forms.ModelForm):
    class Meta:
        model = problem
        fields = ('problem','room','reporter','urgency')
        widgets = {
            'reporter': HiddenInput() ,
            'urgency': TextInput(attrs={'type':'range','min':0,'max':2,'step':1,'value':1,'id':'slider'}),
        }
        labels = {
            "problem":_("Problem"),
            "room":_("Room"),
            "urgency":_("Urgency"),
        }
class ProblemFormGuest(forms.ModelForm):
    class Meta:
        model = problem
        fields = ('reporter_guest','problem','room','urgency')
        widgets = {
            'urgency': TextInput(attrs={'type':'range','min':0,'max':2,'step':1,'value':1,'id':'slider'}),
        }
        labels = {
            "reporter_guest":_("Name"),
            "problem":_("Problem"),
            "room":_("Room"),
            "urgency":_("Urgency"),
        }