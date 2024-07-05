from timetable import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('report/',views.reportAbsence,name='reportAbsence'),
    path('setSub/',views.sub),
    path('get/<int:n>/',views.get_possible_subs,name='possible subs'),
    path('user/register', views.register, name='register'),
]