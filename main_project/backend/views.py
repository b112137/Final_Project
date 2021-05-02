from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timezone
from django.views.generic import View
import json
from backend.models import Chat
from backend.models import Profile, Mission_imformation, Mission_group, Mission_Chatroom

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

def chatroom_page(request):
    return render(request, 'chatroom.html', {
    })


def register_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        account = request.POST.get('account')
        password = request.POST.get('password')
        sex = request.POST.get('sex')
        birth = request.POST.get('birth')
        
        print(len(Profile.objects.filter(account=account)))
        if len(Profile.objects.filter(account=account)) == 0:
            Profile.objects.create(name=name, account=account, password=password, sex=sex, birth=birth,\
                                    exp1=0, exp2=0, exp3=0, balance=0, character_name="test.jpg", profile_photo="none.jpg",\
                                    mission_doing_chatroom_ID=[], mission_done_chatroom_ID=[], friend_ID=[], owned_product_ID=[]
            )
            return JsonResponse({
                'result' : "success",
            })
        else:
            return JsonResponse({
                'result' : "account_exist",
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
        # print(mission_imformation)
        mission_all = core_serializers.serialize("json", mission_imformation)
        mission_all = json.loads(mission_all)

        mission_ID, mission_name, mission_pic, joined, mission_intro, mission_type, group_required, exp1, exp2, exp3, reward = [], [], [], [], [], [], [], [], [], [], []
        for mission in mission_all:
            mission_ID.append(mission['fields']['mission_ID'])
            mission_name.append(mission['fields']['mission_name'])
            mission_pic.append(mission['fields']['mission_pic'])
            joined.append(mission['fields']['joined'])
            mission_intro.append(mission['fields']['mission_intro'])
            mission_type.append(mission['fields']['mission_type'])
            group_required.append(mission['fields']['group_required'])
            exp1.append(mission['fields']['exp1'])
            exp2.append(mission['fields']['exp2'])
            exp3.append(mission['fields']['exp3'])
            reward.append(mission['fields']['reward'])

        # print(mission_ID, mission_name, mission_pic, joined, mission_intro, mission_type, group_required, exp1, exp2, exp3, reward)


        return JsonResponse({
            'result' : "success",
            "mission_ID":mission_ID, "mission_name":mission_name, "mission_pic":mission_pic,
            "joined":joined, "mission_intro":mission_intro, "mission_type":mission_type, "group_required":group_required,
            "exp1":exp1, "exp2":exp2, "exp3":exp3, "reward":reward
        })

def get_all_mission_img(request):
    if request.method == 'POST':
        img_path = request.POST.get('img_path')
        image = cv2.imread(img_path)
        image = cv2.imencode('.jpg',image)[1]
        back_2 = base64.b64encode(image)

        return HttpResponse(back_2)

def get_mission_group(request):
    if request.method == 'POST':
        account = request.POST.get("user_ID")
        mission_ID = request.POST.get('mission_ID')

        chatroom_ID, group_name, group_now, group_most, leader_ID = mission_filter(account, mission_ID)

        return JsonResponse({
            'result' : "success",
            "chatroom_ID": chatroom_ID, "group_name": group_name, "group_now": group_now,
            "group_most": group_most, "leader_ID": leader_ID
        })

def join_mission_group(request):
    if request.method == 'POST':
        account = request.POST.get("user_ID")
        mission_ID = request.POST.get('mission_ID')
        chatroom_ID = request.POST.get('chatroom_ID')

        ### 修改 mission group
        group_search_all = Mission_group.objects.filter(chatroom_ID=chatroom_ID)
        group_search = group_search_all[0]
        if group_search.status == "acceptable":
            member_ID = ast.literal_eval(group_search.member_ID)
            member_ID.append(account)
            group_search_all.update(member_ID = member_ID)

            if len(member_ID) >= int(group_search.group_most):
                group_search_all.update(status = "full")
        
        ### 修改 mission imformation
        mission_search_all = Mission_imformation.objects.filter(mission_ID=mission_ID)
        mission_search = mission_search_all[0]
        joined = mission_search.joined
        joined = int(joined) + 1
        mission_search_all.update(joined = joined)

        joined_ID = ast.literal_eval(mission_search.joined_ID)
        joined_ID.append(account)
        mission_search_all.update(joined_ID = joined_ID)

        ### 修改 Profile
        profile_search_all = Profile.objects.filter(account=account)
        profile_search = profile_search_all[0]
        mission_doing_chatroom_ID = ast.literal_eval(profile_search.mission_doing_chatroom_ID)
        mission_doing_chatroom_ID.append(chatroom_ID)
        profile_search_all.update(mission_doing_chatroom_ID = mission_doing_chatroom_ID)
        
        ### 取得刷新頁面資料
        chatroom_ID, group_name, group_now, group_most, leader_ID = mission_filter(account, mission_ID)

        return JsonResponse({
            'result' : "success",
            "chatroom_ID": chatroom_ID, "group_name": group_name, "group_now": group_now,
            "group_most": group_most, "leader_ID": leader_ID
        })

def create_mission_group(request):
    if request.method == 'POST':
        group_name = request.POST.get("group_name")
        mission_ID = request.POST.get('mission_ID')
        leader_ID = request.POST.get('leader_ID')
        group_most = request.POST.get('group_most')

        group_required = Mission_imformation.objects.filter(mission_ID=mission_ID)[0].group_required
        if group_required > group_most:
            return JsonResponse({
                'result' : "least_than_group_required",
            })

        ### 新增 mission group 欄位
        lastest_chatroom_ID = int(Mission_group.objects.order_by('pk').last().chatroom_ID) + 1
        mission_name = Mission_imformation.objects.filter(mission_ID=mission_ID)[0].mission_name
        status = "acceptable"
        member_ID = [leader_ID]
        
        Mission_group.objects.create(chatroom_ID=lastest_chatroom_ID, mission_ID=mission_ID, mission_name=mission_name,
            group_name=group_name, group_most=group_most, leader_ID=leader_ID, status=status, member_ID=member_ID
        )

        ### 修改 mission imformation
        mission_search_all = Mission_imformation.objects.filter(mission_ID=mission_ID)
        mission_search = mission_search_all[0]
        joined = mission_search.joined
        joined = int(joined) + 1
        mission_search_all.update(joined = joined)

        joined_ID = ast.literal_eval(mission_search.joined_ID)
        joined_ID.append(leader_ID)
        mission_search_all.update(joined_ID = joined_ID)

        ### 修改 Profile
        profile_search_all = Profile.objects.filter(account=leader_ID)
        profile_search = profile_search_all[0]
        mission_doing_chatroom_ID = ast.literal_eval(profile_search.mission_doing_chatroom_ID)
        mission_doing_chatroom_ID.append(lastest_chatroom_ID)
        profile_search_all.update(mission_doing_chatroom_ID = mission_doing_chatroom_ID)

        return JsonResponse({
            'result' : "success",
        })


def get_mission_chatroom(request):
    if request.method == 'POST':
        account = request.POST.get("account")
        profile_search_all = Profile.objects.filter(account=account)
        profile_search = profile_search_all[0]
        mission_doing_chatroom_ID = ast.literal_eval(profile_search.mission_doing_chatroom_ID)
        mission_done_chatroom_ID = ast.literal_eval(profile_search.mission_done_chatroom_ID)

        chatroom_ID_all, mission_ID, mission_name, group_name, status, message, time = [], [], [], [], [], [], []
        for chatroom_ID in mission_doing_chatroom_ID:
            chatroom_ID_all.append(chatroom_ID)

            group_search = Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0]
            mission_ID.append(group_search.mission_ID)
            mission_name.append(group_search.mission_name)
            group_name.append(group_search.group_name)
            status.append(group_search.status)

            lastest_message = Mission_Chatroom.objects.filter(chatroom_ID=chatroom_ID).order_by('pk').last()

            if lastest_message:
                message.append(lastest_message.message)
                time.append(lastest_message.time)
                # print(lastest_message.time)
            else:
                message.append("")
                time.append(datetime(1999, 3, 26, 0, 0, 0, 0, tzinfo=timezone.utc))

        # print(chatroom_ID_all, mission_ID, mission_name, group_name, status, message, time)
        time_copy = time.copy()

        time, chatroom_ID_all = (list(t) for t in zip(*sorted(zip(time_copy, chatroom_ID_all), reverse=True  )))
        time, mission_ID = (list(t) for t in zip(*sorted(zip(time_copy, mission_ID), reverse=True  )))
        time, mission_name = (list(t) for t in zip(*sorted(zip(time_copy, mission_name), reverse=True  )))
        time, group_name = (list(t) for t in zip(*sorted(zip(time_copy, group_name), reverse=True  )))
        time, status = (list(t) for t in zip(*sorted(zip(time_copy, status), reverse=True  )))
        time, message = (list(t) for t in zip(*sorted(zip(time_copy, message), reverse=True  )))


        # print(chatroom_ID_all, mission_ID, mission_name, group_name, status, message, time)




        return JsonResponse({
            'result' : "success",
            "chatroom_ID": chatroom_ID_all, "mission_ID": mission_ID, "mission_name": mission_name,
            "group_name": group_name, "status": status, "message": message, "time": time
        })

def mission_chat_update(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == "Send":
            room = request.POST.get('room')
            user = request.POST.get('user')
            content = request.POST.get('content')
            print(content)
            with open('msg.txt', 'a', encoding="utf-8") as msg_file:
                msg_file.write( content+'\n' )
                msg_file.close()

            Chat.objects.create(room=room, user=user,  content=content)
            return JsonResponse({
                'result' : "success"
            })

        elif post_type == "Receive":
            
            chatroom_ID = request.POST.get('chatroom_ID')   
            print(chatroom_ID)
            history = core_serializers.serialize("json", Mission_Chatroom.objects.filter(chatroom_ID=chatroom_ID).order_by("time"))
            print(history)

            return JsonResponse({
                'result' : "success",
                'history' : history,
                # 'room_history' : room_history,
            })



def get_profile(account):
    profile = Profile.objects.filter(account=account)
    return profile


def mission_filter(account, mission_ID):
    group_search = Mission_group.objects.filter(mission_ID=mission_ID)

    mission_doing_chatroom_ID = Profile.objects.filter(account=account)[0].mission_doing_chatroom_ID
    mission_doing_chatroom_ID = ast.literal_eval(mission_doing_chatroom_ID)

    chatroom_ID, group_name, group_now, group_most, leader_ID = [], [], [], [], []
    for group in group_search:
        check = 0
        for my_chatroom_ID in mission_doing_chatroom_ID: 
            if group.chatroom_ID == my_chatroom_ID:
                check = 1
                break
        if check == 0: #沒參加過
            if group.status == "acceptable":
                chatroom_ID.append(group.chatroom_ID)
                group_name.append(group.group_name)
                group_now.append(len( ast.literal_eval(group.member_ID) ))
                group_most.append(group.group_most)
                leader_ID.append(group.leader_ID)

    return chatroom_ID, group_name, group_now, group_most, leader_ID






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

