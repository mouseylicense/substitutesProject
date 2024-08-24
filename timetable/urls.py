from timetable import views
from django.urls import path, include

from timetable.views import get_student_list

urlpatterns = [
    path('', views.index, name='index'),
    path('student/details/<slug:uuid>',views.student_details, name='student_details'),
    path('student/register/',views.register_student, name='register_student'),
    path('teacher/manage_students/',views.student_manager, name='student_manager'),
    path('teacher/setSub/',views.sub,name='sub'),
    path('get/<int:n>/',views.get_possible_subs,name='possible subs'),
    path('teacher/user/details/<uuid:uuid>', views.register, name='register'),
    path('schedule/setClasses/',views.setClasses,name='setClasses'),
    path('getRoom/',views.get_possible_rooms,name='possible_rooms'),
    path('getClasses/<int:n>',views.get_teacher_classes,name='get_classes'),
    path('timetable/',views.timetable,name='timetable'),
    path('schedule/set_schedule/<slug:uuid>',views.set_schedule,name='schedule'),
    path('send_email/',views.send_email,name='send_email'),
    path('print/',views.printable,name='print'),
    path('managment/teachers',views.teacher_manager, name='teacher_manager'),
    path('managment/invite_teacher/',views.create_teacher,name='create_teacher'),
    path('teacher/home/',views.teacher_home,name="teacher_home"),
    path('delete_absence/',views.delete_absence,name='delete_absence'),
    path('managment/danger_zone/',views.danger_zone,name='danger_zone'),
    path('teacher/classes_manager/',views.class_manager,name='class_manager'),
    path('managment/import/',views.import_page,name='import'),
    path('getDecriptionForm',views.editDescription,name='editDescription'),
    path('getStudents/<slug:id>',views.get_student_list,name='get_student_list')
]