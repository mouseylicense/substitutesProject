from slack import views
from django.urls import path, include


urlpatterns = [
    path('',views.resolve_problem,name='api'),
    path("link",views.link_account,name='id'),
    path("fix",views.fix_problems,name='fix'),
]