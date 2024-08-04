from django.contrib import admin
from . import models
# Register your models here.


class ClassAdmin(admin.ModelAdmin):
    fields = ['name',('day_of_week','hour'),'room','teacher',('student_teacher','student_teaching'),('first_grade','second_grade','third_grade','fourth_grade','fifth_grade','sixth_grade','seventh_grade','eighth_grade','ninth_grade','tenth_grade','eleventh_grade','twelfth_grade')]


class TeacherAdmin(admin.ModelAdmin):
    fields = ['username',('email','phone_number'),'can_substitute',('Sunday','Monday','Tuesday','Wednesday','Thursday'),('user_permissions','groups','is_superuser','password','is_staff')]
admin.site.register(models.Teacher,TeacherAdmin)
admin.site.register(models.Class,ClassAdmin)
admin.site.register(models.Absence)
admin.site.register(models.ClassNeedsSub)
admin.site.register(models.Room)
class StudentAdmin(admin.ModelAdmin):
    fields = ["uuid","name","email","phone_number","grade","tutor","shacharit"]
    readonly_fields = ["uuid"]
admin.site.register(models.Student,StudentAdmin)