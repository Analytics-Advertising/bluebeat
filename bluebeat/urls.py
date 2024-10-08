"""
URL configuration for bluebeat project.

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
from django.contrib import admin
from django.urls import path, include
from system_management import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_application, name='application-home'),
    path('system_management/', include('system_management.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/home/', views.redirect_user, name='redirect-user'),
    path('dealer/', include('dealer.urls')),
    path('Administrator/', include('bluebeat_admin.urls')),

]
