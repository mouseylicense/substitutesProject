from timetable import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('report/',views.reportAbsence,name='report'),
    path('setSub/',views.sub)
]