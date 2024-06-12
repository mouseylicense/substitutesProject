from timetable import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('report/',views.reportAbsence,name='report'),
    path('setSub/',views.sub),
    path('get/<int:n>/',views.get_possible_subs,name='possible subs'),
]