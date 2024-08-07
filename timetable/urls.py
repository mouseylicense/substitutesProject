from timetable import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('teacher/report/',views.reportAbsence,name='reportAbsence'),
    path('teacher/setSub/',views.sub,name='sub'),
    path('get/<int:n>/',views.get_possible_subs,name='possible subs'),
    path('teacher/user/register', views.register, name='register'),
    path('teacher/mySubs/',views.mySubs,name='mySubs'),
    path('schedule/setClasses/',views.setClasses,name='setClasses'),
    path('getRoom/',views.get_possible_rooms,name='possible_rooms'),
    path('getClasses/<int:n>',views.get_teacher_classes,name='get_classes'),
    path('timetable/',views.timetable,name='timetable'),
    path('schedule/set_schedule/<slug:uuid>',views.set_schedule,name='schedule'),
    path('schedule/manage_schedules',views.schedule_manager, name='schedule_manager'),
    path('send_email/',views.send_email,name='send_email'),
]