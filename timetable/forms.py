from _ast import Sub
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms import DateInput, Select, TextInput
from django.utils.translation import gettext_lazy as _


class AbsenceForm(forms.Form):
    date = forms.DateField(label=_("Date"), widget=DateInput(attrs={'class': 'datepicker', 'type': 'date'}))
    reason = forms.CharField(label=_("Reason"),
                             widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('Reason')}))



class ClassForm(forms.ModelForm):
    name = forms.CharField(label=_("Subject"),widget=forms.TextInput(attrs={'class': 'subject-input', 'placeholder': _('Subject')}))
    teacher = forms.ModelChoiceField(Teacher.objects,label=_("Teacher"),widget=forms.Select(attrs={"style":"flex-grow:1",'class': 'select','id':'teacher'}))
    day_of_week = forms.CharField(label=_("Day"),widget=forms.TextInput(attrs={"required":"","onkeydown":"return false;","style":"caret-color: transparent !important;pointer-events: none;","id":"day"}))
    hour = forms.CharField(label=_("Hour"),widget=forms.TextInput(attrs={"required":"","id":"hour","onkeydown":"return false;","style":"caret-color: transparent !important;pointer-events: none;"}))
    room = forms.ModelChoiceField(Room.objects,widget=forms.Select(attrs={'id': 'room',"disabled":""}))
    class Meta:
        model = Class
        fields = ("teacher","name","day_of_week","hour","room")

class SubstituteForm(forms.Form):
    class_that_needs_sub = forms.ModelChoiceField(
        ClassNeedsSub.objects.order_by('substitute_teacher__username', 'date'),
        label=_("Class that needs sub"),
        widget=forms.Select(attrs={'id': 'sub'}), empty_label=None)
    substitute_teacher = forms.CharField(widget=forms.Select(attrs={'id': 'teacher'}))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput, min_length=8)
    phone_number = forms.CharField(label=_('Phone'),
                                   widget=forms.TextInput(attrs={'type': 'tel', "pattern": "[0-9]{10}"}),
                                   min_length=10, max_length=10)
    name = forms.CharField(label=_("Name"))
    email = forms.EmailField(label=_("Email"))
    class Meta:
        model = Teacher
        fields = ('username', 'email', 'phone_number', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user

