"""
URL configuration for appleEmobilisFinalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import include, path
from . import views as my_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls, name='unique_admin_namespace'),
    path('', my_views.home, name='home-url'),
    path('auth/', include('auth.urls')),
    path('dashbord/', include('dashbord.urls')),
    path('user_auth/', include('user_auth.urls')),
    path('dashboard/', my_views.dashboard, name='dashboard-url'),
    path('admin_app/', include('admin_app.urls')),
    path('contact/',my_views.contact,name='contact-url'),
]