from LaptopLoaning import views
from django.urls import path
urlpatterns = [
    path('check_pin/', views.check_pin, name='check_pin'),
    path('home/', views.laptops_home, name='laptop_home')
]