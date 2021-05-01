from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.views.generic import View
import json
from backend.models import Chat
from backend.models import Profile, Mission_imformation

from rest_framework import serializers
from django.core import serializers as core_serializers
import ast 
import cv2
import base64

# Create your views here.
def start_page(request):
    time = datetime.now()
    return render(request, 'start.html', {
        'datetime': time
    })

def login_page(request):
    time = datetime.now()
    return render(request, 'login.html', {
        'datetime': time
    })

def register_page(request):
    time = datetime.now()
    return render(request, 'register.html', {
        'datetime': time
    })

def main_page(request):
    account = request.GET.get("account")
    profile = get_profile(account)
    character_name = profile[0].character_name
    name = profile[0].name
    exp1 = profile[0].exp1
    exp2 = profile[0].exp2
    exp3 = profile[0].exp3

    return render(request, 'main.html', {
        'character_name': character_name,
        'name': name,
        'exp1': exp1,
        'exp2': exp2,
        'exp3': exp3,
    })

def mission_page(request):
    return render(request, 'mission.html', {
    })





def register_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        account = request.POST.get('account')
        password = request.POST.get('password')
        sex = request.POST.get('sex')
        birth = request.POST.get('birth')
        Profile.objects.create(name=name, account=account, password=password, sex=sex, birth=birth,\
                                exp1=0, exp2=0, exp3=0, balance=0, character_name="test.jpg", profile_photo="none.jpg",\
                                mission_doing_chatroom_ID=[], mission_done_chatroom_ID=[], friend_ID=[], owned_product_ID=[]
        )

        return JsonResponse({
            'result' : "success",
        })

def login_check(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        profile = get_profile(account)
        # print(profile)

        if profile:  ## 有此帳號
            if profile[0].password == password:
                print("登入成功")
                return JsonResponse({
                    'result' : "success",
                })
            else:
                print("密碼錯誤")
                return JsonResponse({
                    'result' : "password_error",
                })
        else: 
            print("無此帳號")
            return JsonResponse({
                'result' : "not_found",
            })


def get_all_mission(request):
    if request.method == 'POST':
        mission_imformation = Mission_imformation.objects.all()
        print(mission_imformation)
        mission_all = core_serializers.serialize("json", mission_imformation)
        mission_all = json.loads(mission_all)

        mission_ID, mission_name, mission_pic, joined, mission_intro, mission_type, exp1, exp2, exp3, reward = [], [], [], [], [], [], [], [], [], []
        for mission in mission_all:
            mission_ID.append(mission['fields']['mission_ID'])
            mission_name.append(mission['fields']['mission_name'])
            mission_pic.append(mission['fields']['mission_pic'])
            joined.append(mission['fields']['joined'])
            mission_intro.append(mission['fields']['mission_intro'])
            mission_type.append(mission['fields']['mission_type'])
            exp1.append(mission['fields']['exp1'])
            exp2.append(mission['fields']['exp2'])
            exp3.append(mission['fields']['exp3'])
            reward.append(mission['fields']['reward'])

        print(mission_ID, mission_name, mission_pic, joined, mission_intro, mission_type, exp1, exp2, exp3, reward)


        return JsonResponse({
            'result' : "success",
            "mission_ID":mission_ID, "mission_name":mission_name, "mission_pic":mission_pic,
            "joined":joined, "mission_intro":mission_intro, "mission_type":mission_type,
            "exp1":exp1, "exp2":exp2, "exp3":exp3, "reward":reward
        })

def get_all_mission_img(request):
    if request.method == 'POST':
        mission_imformation = Mission_imformation.objects.all()
        mission_all = core_serializers.serialize("json", mission_imformation)
        mission_all = json.loads(mission_all)
        mission_pic = []
        for mission in mission_all:
            mission_pic.append(mission['fields']['mission_pic'])
        print("/media/mission_img/"+mission_pic[0])
        image = cv2.imread("media/mission_img/"+mission_pic[0])
        
        image = cv2.imencode('.jpg',image)[1]
        back_2 = base64.b64encode(image)


        # print(back_2)
        return HttpResponse(back_2)


def get_profile(user_ID):
    profile = Profile.objects.filter(account=user_ID)
    
    return profile



# def modify_profile(request):
# #     if request.method == 'POST':
# #         profile_1 = Profile.objects.filter(account="bladebaby0326")
# #         text = profile_1[0].friend_ID
# #         text_list = ast.literal_eval(text)
# #         text_list.append("test2")
# #         profile_1.update(friend_ID = text_list)

#         return JsonResponse({
#             'result' : "success",
#         })

# def chat_update(request):
#     if request.method == 'POST':
#         post_type = request.POST.get('post_type')
#         if post_type == "Send":
#             room = request.POST.get('room')
#             user = request.POST.get('user')
#             content = request.POST.get('content')
#             print(content)
#             with open('msg.txt', 'a', encoding="utf-8") as msg_file:
#                 msg_file.write( content+'\n' )
#                 msg_file.close()

#             Chat.objects.create(room=room, user=user,  content=content)
#             return JsonResponse({
#                 'result' : "success"
#             })

#         elif post_type == "Receive":
#             room = request.POST.get('room')

#             history = []
#             with open('msg.txt', 'r', encoding="utf-8") as msg_file:
#                 line = msg_file.readline()
#                 while line:
#                     history.append(line)
#                     line = msg_file.readline()
#                 msg_file.close()

#             # room_history = core_serializers.serialize("json", Chat.objects.all())
#             room_history = core_serializers.serialize("json", Chat.objects.filter(room=room).order_by("time"))
#             print(room_history)

#             return JsonResponse({
#                 'result' : "success",
#                 'msg' : history,
#                 'room_history' : room_history,
#             })

