"""
URL configuration for SubtitutesProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.urls import include, path,re_path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
import timetable.forms
urlpatterns = [
    # Needed for locale change
    path('i18n/', include('django.conf.urls.i18n')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),

    path('', include('timetable.urls')),
    path('teacher/user/', include('django.contrib.auth.urls')),
    re_path('teacher/user/login', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=timetable.forms.CustomAuthForm,redirect_authenticated_user=True),
         name='login')

)
if settings.LAPTOPS_ENABLED:
    urlpatterns += i18n_patterns(path('laptops/', include('LaptopLoaning.urls')))
