from timetable import views
from django.urls import path
urlpatterns = [
    path('', views.index, name='index'),
    path('get/<slug:teacher>/',views.retrieve_classes,name='retrieve_classes'),
    path('sub/',views.absences)
]