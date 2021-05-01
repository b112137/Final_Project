"""main_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.views.generic import TemplateView
import backend.views as backend

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name="start.html")),
    path('start', backend.start_page),
    path('login', backend.login_page),
    path('register', backend.register_page),
    path('main', backend.main_page),
    path('mission', backend.mission_page),
    
    path('register_submit', backend.register_submit),
    path('login_check', backend.login_check),
    path('get_all_mission', backend.get_all_mission),
    path('get_all_mission_img', backend.get_all_mission_img),


    # path('chat_update', backend.chat_update),
]
