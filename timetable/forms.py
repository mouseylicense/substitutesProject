from _ast import Sub

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import *
from django.forms import DateInput, Select, TextInput, HiddenInput, PasswordInput
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
    teachers = forms.ModelMultipleChoiceField(Teacher.objects.filter(type=0).only("pk","first_name","last_name"),required=False,label=_("Teachers"),widget=forms.SelectMultiple(attrs={'id':'teacher','class':'select form-select selectpicker'}))
    day_of_week = forms.CharField(label=_("Day"),widget=forms.TextInput(attrs={"required":"","onkeydown":"return false;","style":"caret-color: transparent !important;pointer-events: none;","id":"day"}))
    hour = forms.CharField(label=_("Hour"),widget=forms.TextInput(attrs={"required":"","id":"hour","onkeydown":"return false;","style":"caret-color: transparent !important;pointer-events: none;"}))
    room = forms.ModelChoiceField(Room.objects.only("pk","name"),widget=forms.Select(attrs={'id': 'room',"disabled":""}))
    student_teacher = forms.BooleanField(required=False,label=_("Is a Student Teaching?"),widget=forms.CheckboxInput(attrs={"onclick":'toggleTeacherStudent(this);','class':'checkbox','id':'isAStudentTeaching'}))
    student_teaching = forms.CharField(required=False,widget=TextInput(attrs={'placeholder':_("Student Teaching"),'hidden':'','class':'subject-input','id':'studentTeaching'}))
    class Meta:
        model = Class
        fields = "__all__"
        widgets= {
            "max_students":forms.HiddenInput(),
            "description":forms.Textarea(attrs={'placeholder':_("Description")+"...",'style':'flex-grow:1'}),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = "__all__"
        widgets={
            "student":HiddenInput(),
        }
        labels = {
            "sunday_first": _("Sunday") + " 09:15",
            "sunday_second": _("Sunday") + " 10:07",
            "sunday_third": _("Sunday") + " 11:45",
            "sunday_fourth": _("Sunday") + " 12:45",
            "sunday_ld": _("Sunday") + " " + _("Long Day"),

            "monday_first": _("Monday") + " 09:15",
            "monday_second": _("Monday") + " 10:07",
            "monday_third": _("Monday") + " 11:45",
            "monday_fourth": _("Monday") + " 12:45",
            "monday_ld": _("Monday") + " " + _("Long Day"),

            "tuesday_first": _("Tuesday") + " 09:15",
            "tuesday_second": _("Tuesday") + " 10:07",
            "tuesday_third": _("Tuesday") + " 11:45",
            "tuesday_fourth": _("Tuesday") + " 12:45",
            "tuesday_ld": _("Tuesday") + " " + _("Long Day"),

            "wednesday_first": _("Wednesday") + " 09:15",
            "wednesday_second": _("Wednesday") + " 10:07",
            "wednesday_third": _("Wednesday") + " 11:45",
            "wednesday_fourth": _("Wednesday") + " 12:45",
            "wednesday_ld": _("Wednesday") + " " + _("Long Day"),

            "thursday_first": _("Thursday") + " 09:15",
            "thursday_second": _("Thursday") + " 10:07",
            "thursday_third": _("Thursday") + " 11:45",
            "thursday_fourth": _("Thursday") + " 12:45",
            "thursday_ld": _("Thursday") + " " + _("Long Day"),

        }
    def __init__(self, *args, **kwargs):
        print(args)
        student = args[0]['student']
        # student = False
        super().__init__(*args, **kwargs)
        filter_query = {NUMBERS_TO_GRADES[Student.objects.get(pk=student).grade]:True}
        if student:
            ld = ["sunday_ld","monday_ld","tuesday_ld","wednesday_ld","thursday_ld"]
            recess = ["sunday_recess","monday_recess","tuesday_recess","wednesday_recess","thursday_recess"]


            excluded_classes = Class.objects.filter(**filter_query)
            for field_name in self.fields:
                if field_name.startswith('sunday_') or field_name.startswith('monday_') or \
                        field_name.startswith('tuesday_') or field_name.startswith('wednesday_') or \
                        field_name.startswith('thursday_'):
                    self.fields[field_name].queryset = self.fields[field_name].queryset.filter(**filter_query)

            # This is an option to hide fields with no choice:
            # for field_name,field in self.fields.items():
            #     if len(field.choices)<=1:
            #         field.widget = HiddenInput()
            #     print(field_name)

            # This hides the longday and recess fields if they are empty:
            for day in range(0,5):
                if len(self.fields[ld[day]].choices)<=1:
                    self.fields[ld[day]].widget = HiddenInput()
                if len(self.fields[recess[day]].choices)<=1:
                    self.fields[recess[day]].widget = HiddenInput()




class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('first_name','last_name', 'phone_number', 'password','Sunday','Monday','Tuesday','Wednesday','Thursday')
        widgets = {
            "first_name":forms.TextInput(attrs={'placeholder': _('First Name')}),
            "last_name":forms.TextInput(attrs={'placeholder':_('Last Name')}),
            "password":forms.PasswordInput(attrs={'placeholder':_('Password'),"min_length":"8"}),
            "phone_number":forms.TextInput(attrs={'placeholder':_('Phone Number'),'type':'tel', "pattern": "[0-9]{10}","min_length":"10","max_length":"10"}),
        }
        labels = {
            "Sunday":_("Sunday"),
            "Monday":_("Monday"),
            "Tuesday":_("Tuesday"),
            "Wednesday":_("Wednesday"),
            "Thursday":_("Thursday"),
            "phone_number":_("Phone Number"),
            "password":_("Password"),
            "first_name":_("First Name"),
            "last_name":_("Last Name"),
        }
    def save(self, commit=True):
        # Save the provided password in hashed format

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user

class TeacherForm(forms.ModelForm):
    uuid = forms.UUIDField(widget=forms.HiddenInput())

    class Meta:
        model = Teacher
        fields = ("Sunday","Monday","Tuesday","Wednesday","Thursday","tutor","shocher",
                  "can_substitute","manage_subs","manage_schedule")

        labels = {
            "Sunday":_("Sunday"),
            "Monday":_("Monday"),
            "Tuesday":_("Tuesday"),
            "Wednesday":_("Wednesday"),
            "Thursday":_("Thursday"),
            "tutor":_("Tutor"),
            "shocher":_("Shocher"),
            "can_substitute":_("Substitutes?"),
            "manage_subs":_("Manages Subs"),
            "manage_schedule":_("Manages Schedule")
        }


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': _('Email')}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':_('Password')}))

class SuperuserCreationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('first_name','last_name','email','password','phone_number')
        widgets = {
            "first_name": forms.TextInput(attrs={'placeholder': _('First Name')}),
            "last_name": forms.TextInput(attrs={'placeholder': _('Last Name')}),
            "email": forms.EmailInput(attrs={'placeholder': _('Email')}),
            "password": forms.PasswordInput(attrs={'placeholder': _('Password'), "min_length": "8"}),
            "phone_number": forms.TextInput(
                attrs={'placeholder': _('Phone Number'), 'type': 'tel', "pattern": "[0-9]{10}", "min_length": "10",
                       "max_length": "10"}),
        }
        labels = {
            "phone_number": "",
            "password": "",
            "first_name": "",
            "last_name": "",
            "email": ""
        }

    def save(self, commit=True):
        # Save the provided password in hashed format

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        if commit:
            user.save()

        return user


class StudentRegistrationForm(forms.ModelForm):
    uuid = forms.UUIDField(widget=forms.HiddenInput(),initial=uuid.uuid4())
    class Meta:
        model = Student
        fields = ("name","email","phone_number","grade")
        widgets = {
            "name": forms.TextInput(attrs={'placeholder': _('Name')}),
            "email": forms.EmailInput(attrs={'placeholder': _('Email')}),
            "phone_number": forms.TextInput(
                attrs={'placeholder': _('Phone Number'), 'type': 'tel', "pattern": "[0-9]{10}", "min_length": "10",
                       "max_length": "10"}),
        }

class DescriptionChangeForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Class
        fields = ('description',)
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': _('Description')})
        }

class UploadFileForm(forms.Form):
    fileFor = forms.ChoiceField(choices=[(0,'teachers'),(1,"students")],widget=forms.HiddenInput())
    file = forms.FileField(label=_('Select a file'))