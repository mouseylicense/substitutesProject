from dashboard import views
from django.urls import path, include


urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('stats',views.stats,name='dashboard_stats'),
    path('report',views.report, name='report'),
    path('data',views.data, name='data'),
    path('home',views.home,name='dashboard_home'),
    path('problems',views.problems,name='all_problems'),
    path('change_assignee',views.change_assignee,name='change_assignee'),
    path('resolve_problem',views.resolve,name='resolve_problem'),
    path('thank_you',views.thank_you, name="thank_you")
]