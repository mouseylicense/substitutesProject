from slack import views
from django.urls import path, include


urlpatterns = [
    path('',views.interactions,name='api'),
    path("link",views.link_account,name='id'),
    path("fix",views.fix_problems,name='fix'),
    path("door_open",views.door_open,name='door_open'),
    path("otp",views.otp,name='otp'),
]