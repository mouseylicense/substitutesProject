from LaptopLoaning import views
from django.urls import path
urlpatterns = [
    path('home/', views.home, name='laptop_home'),
    path('pin_manager/',views.pin_manager, name='pin_manager'),
    path('available/',views.returnAvailable, name='available_laptops'),
    path('stats/',views.stats, name='stats'),
]