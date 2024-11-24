from dashboard import views
from django.urls import path, include


urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('stats',views.stats,name='stats'),
    path('report',views.report, name='report'),
]