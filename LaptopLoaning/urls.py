from LaptopLoaning import views
from django.urls import path
urlpatterns = [
    path('check_pin/', views.check_pin, name='check_pin'),
    path('home/', views.home, name='laptop_home'),
    path('pin_manager/',views.pin_manager, name='pin_manager'),
]