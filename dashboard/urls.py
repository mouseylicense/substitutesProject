from dashboard import views
from django.urls import path, include


urlpatterns = [
    path('',views.test,name='index'),
    path('stats',views.stats,name='stats'),
    path('report',views.report, name='report'),
]