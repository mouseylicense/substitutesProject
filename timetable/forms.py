from _ast import Sub
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms import DateInput, Select, TextInput


class AbsenceForm(forms.Form):
    date = forms.DateField(widget=DateInput(attrs={'class': 'datepicker', 'type': 'date'}))
    reason = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': 'Reason'}))


class SubstituteForm(forms.Form):
    class_that_needs_sub = forms.ModelChoiceField(
        ClassNeedsSub.objects.order_by('date').filter(substitute_teacher=None),
        widget=forms.Select(attrs={'id': 'sub'}), empty_label="None selected")
    substitute_teacher = forms.CharField(widget=forms.Select(attrs={'id': 'teacher'}))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8)
    phone_number = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'type': 'tel', "pattern": "[0-9]{10}"}),
                                   min_length=10, max_length=10)

    class Meta:
        model = Teacher
        fields = ('name', 'email', 'phone_number', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user
