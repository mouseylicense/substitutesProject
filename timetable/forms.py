from _ast import Sub
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms import DateInput, Select, TextInput, HiddenInput
from django.utils.translation import gettext_lazy as _

NUMBERS_TO_GRADES = {
    0:"first_grade",
    1:"second_grade",
    2:"third_grade",
    3:"fourth_grade",
    4:"fifth_grade",
    5:"sixth_grade",
    6:"seventh_grade",
    7:"eighth_grade",
    8:"ninth_grade",
    9:"tenth_grade",
    10:"eleventh_grade",
    11:"twelfth_grade",
    12:"Graduate"
}
class AbsenceForm(forms.Form):
    date = forms.DateField(label=_("Date"), widget=DateInput(attrs={'class': 'datepicker', 'type': 'date'}))
    reason = forms.CharField(label=_("Reason"),
                             widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('Reason')}))



class ClassForm(forms.ModelForm):
    name = forms.CharField(label=_("Subject"),widget=forms.TextInput(attrs={'class': 'subject-input', 'placeholder': _('Subject')}))
    teacher = forms.ModelChoiceField(Teacher.objects,required=False,label=_("Teacher"),widget=forms.Select(attrs={"style":"flex-grow:1",'class': 'select','id':'teacher'}))
    day_of_week = forms.CharField(label=_("Day"),widget=forms.TextInput(attrs={"required":"","onkeydown":"return false;","style":"caret-color: transparent !important;pointer-events: none;","id":"day"}))
    hour = forms.CharField(label=_("Hour"),widget=forms.TextInput(attrs={"required":"","id":"hour","onkeydown":"return false;","style":"caret-color: transparent !important;pointer-events: none;"}))
    room = forms.ModelChoiceField(Room.objects,widget=forms.Select(attrs={'id': 'room',"disabled":""}))
    student_teacher = forms.BooleanField(required=False,label=_("Is a Student Teaching?"),widget=forms.CheckboxInput(attrs={"onclick":'toggleTeacherStudent(this);','class':'checkbox','id':'isAStudentTeaching'}))
    student_teaching = forms.CharField(required=False,widget=TextInput(attrs={'placeholder':_("Student Teaching"),'hidden':'','class':'subject-input','id':'studentTeaching'}))
    class Meta:
        model = Class
        fields = "__all__"
        widgets= {
            "description":forms.Textarea(attrs={'placeholder':_("Description")+"...",'style':'flex-grow:1'}),
        }

class SubstituteForm(forms.Form):
    class_that_needs_sub = forms.ModelChoiceField(
        ClassNeedsSub.objects.order_by('substitute_teacher__username', 'date'),
        label=_("Class that needs sub"),
        widget=forms.Select(attrs={'id': 'sub'}), empty_label=None)
    substitute_teacher = forms.CharField(widget=forms.Select(attrs={'id': 'teacher'}))

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = "__all__"
        widgets={
            "student":HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        print(args)
        student = args[0]['student']
        # student = False
        super().__init__(*args, **kwargs)
        filter_query = {NUMBERS_TO_GRADES[Student.objects.get(pk=student).grade]:True}
        if student:
            excluded_classes = Class.objects.filter(**filter_query)
            for field_name in self.fields:
                if field_name.startswith('sunday_') or field_name.startswith('monday_') or \
                        field_name.startswith('tuesday_') or field_name.startswith('wednesday_') or \
                        field_name.startswith('thursday_'):
                    self.fields[field_name].queryset = self.fields[field_name].queryset.filter(**filter_query)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput, min_length=8)
    phone_number = forms.CharField(label=_('Phone'),
                                   widget=forms.TextInput(attrs={'type': 'tel', "pattern": "[0-9]{10}"}),
                                   min_length=10, max_length=10)
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

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ("username","Sunday","Monday","Tuesday","Wednesday","Thursday","tutor","shocher",
                  "can_substitute","manage_subs","manage_schedule")
        widgets = {
            "username":forms.HiddenInput(),
        }
        labels = {
            "Sunday":_("Sunday"),
            "Monday":_("Monday"),
            "Tuesday":_("Tuesday"),
            "Wednesday":_("Wednesday"),
            "Thursday":_("Thursday"),
            "tutor":_("Tutor"),
            "shocher":_("Shocher"),
            "can_substitute":_("Substitutes?"),
        }