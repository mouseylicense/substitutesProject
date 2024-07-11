from timetable import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('report/',views.reportAbsence,name='reportAbsence'),
    path('setSub/',views.sub,name='sub'),
    path('get/<int:n>/',views.get_possible_subs,name='possible subs'),
    path('user/register', views.register, name='register'),
    path('mySubs/',views.mySubs,name='mySubs'),
    path('setClasses/',views.setClasses,name='setClasses'),
    path('getRoom/',views.get_possible_rooms_and_teachers,name='possible_rooms'),
]