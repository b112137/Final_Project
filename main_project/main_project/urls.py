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
    path('chatroom', backend.chatroom_page),
    path('manager', backend.manager_page),
    path('profile', backend.profile_page),
    path('shop', backend.shop_page),

    path('register_submit', backend.register_submit),
    path('login_check', backend.login_check),
    path('get_all_mission', backend.get_all_mission),
    path('get_img', backend.get_img),
    path('get_mission_group', backend.get_mission_group),
    path('join_mission_group', backend.join_mission_group),
    path('create_mission_group', backend.create_mission_group),
    path('get_mission_chatroom_list', backend.get_mission_chatroom_list),
    path('mission_chatroom_update', backend.mission_chatroom_update),
    path('get_mission_chatroom_member', backend.get_mission_chatroom_member),
    path('kick_mission_chatroom_member', backend.kick_mission_chatroom_member),
    path('submit_mission_group_check', backend.submit_mission_group_check),
    path('submit_mission_group', backend.submit_mission_group),
    path('friend_chatroom_update', backend.friend_chatroom_update),
    path('save_profile_intro', backend.save_profile_intro),
    path('get_all_shop', backend.get_all_shop),
    path('buy_product', backend.buy_product),
    
    path('submission_to_finish', backend.submission_to_finish),
    
    
    # 
    path('get_my_mission' , backend.get_my_mission),
    path('get_profile_page' , backend.get_profile_page),
    path('get_main_page' , backend.get_main_page),
    # 
    # path('chat_update', backend.chat_update),



]
