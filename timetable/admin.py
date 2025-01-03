from django.contrib import admin
from . import models
NUMBERS_TO_GRADES = {
    0:"First_Grade",
    1:"Second_Grade",
    2:"Third_Grade",
    3:"Fourth_Grade",
    4:"Fifth_Grade",
    5:"Sixth_Grade",
    6:"Seventh_Grade",
    7:"Eighth_Grade",
    8:"Ninth_Grade",
    9:"Tenth_Grade",
    10:"Eleventh_Grade",
    11:"Twelfth_Grade",
    12:"Graduate"
}
# Register your models here.


class ClassAdmin(admin.ModelAdmin):
    fields = [('name','description'),('day_of_week','hour'),'room','teachers',('student_teacher','student_teaching'),('first_grade','second_grade','third_grade','fourth_grade','fifth_grade','sixth_grade','seventh_grade','eighth_grade','ninth_grade','tenth_grade','eleventh_grade','twelfth_grade'),('visible',)]


class TeacherAdmin(admin.ModelAdmin):
    fields = [('first_name','last_name'),('email','phone_number','slack_id'),('can_substitute','tutor','shocher'),('Sunday','Monday','Tuesday','Wednesday','Thursday'),('user_permissions','groups','is_superuser','password','is_staff','manage_schedule','manage_subs','type','last_sub')]
admin.site.register(models.Teacher,TeacherAdmin)
admin.site.register(models.Class,ClassAdmin)
admin.site.register(models.Absence)
admin.site.register(models.ClassNeedsSub)
admin.site.register(models.Room)



@admin.action(description='Change Student grade and remove Graduates')
def grow_grade(modeladmin, request, queryset):
    for c in queryset:
        c.increment_grade()


class StudentAdmin(admin.ModelAdmin):
    fields = ["uuid","name","email","phone_number","grade","tutor","shacharit","last_schedule_invite"]
    readonly_fields = ["uuid"]
    actions = [grow_grade]


admin.site.register(models.Student,StudentAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    fields = ['student',('sunday_first', 'sunday_second', 'sunday_third', 'sunday_fourth'),
                ('monday_first', 'monday_second', 'monday_third', 'monday_fourth'),
                ('tuesday_first', 'tuesday_second', 'tuesday_third', 'tuesday_fourth'),
                ('wednesday_first', 'wednesday_second', 'wednesday_third', 'wednesday_fourth'),
                ('thursday_first', 'thursday_second')]
admin.site.register(models.Schedule,ScheduleAdmin)