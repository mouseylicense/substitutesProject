from dashboard import views
from django.urls import path, include


urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('stats',views.stats,name='dashboard_stats'),
    path('report',views.report, name='report'),
    path('data',views.data, name='data'),
    path('home',views.home,name='dashboard_home'),
    path('resolve_problem',views.resolve,name='resolve_problem'),
]