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
    class Meta:
        model = Class
        fields = "__all__"
        widgets = {
            "day_of_week": Select(attrs={'id' : 'day_of_week'}),
            "hour": Select(attrs={'id' : 'hour'}),
            "room": Select(attrs={'id' : 'room'}),
        }

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

