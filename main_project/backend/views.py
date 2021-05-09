from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timezone
from django.views.generic import View
import json
from backend.models import Chat
from backend.models import Profile, Mission_imformation, Mission_group, Mission_Chatroom, Mission_submission, Friend_Chatroom

from rest_framework import serializers
from django.core import serializers as core_serializers
import ast 
import cv2
import base64
import random

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
    profile = get_profile(account)[0]

    exp = int(profile.exp1) + int(profile.exp2) + int(profile.exp3)
    level = 1
    exp_temp = exp
    for i in range(1, 200):
        exp_temp -= i*10
        if exp_temp >= 0:
            level += 1
        else:
            exp_temp += i*10
            break

    exp1 = (int(profile.exp1)/exp)*100
    exp2 = (int(profile.exp2)/exp)*100
    exp3 = 100 - exp1 - exp2

    print(exp1, exp2, exp3)

    # name = profile[0].name
    # exp1 = profile[0].exp1
    # exp2 = profile[0].exp2
    # exp3 = profile[0].exp3

    return render(request, 'main.html', {
        # 'character_name': character_name,
        'name': profile.name,
        'level': level,
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

def profile_page(request):
    account = request.GET.get("account")
    profile = Profile.objects.filter(account=account)[0]
    # return JsonResponse({
        
    # })
    exp = int(profile.exp1) + int(profile.exp2) + int(profile.exp3)
    level = 1
    exp_temp = exp
    for i in range(1, 200):
        exp_temp -= i*10
        if exp_temp >= 0:
            level += 1
        else:
            exp_temp += i*10
            break

    Max = max(int(profile.exp1), int(profile.exp2), int(profile.exp3))
    print(Max)
    Max_lenth = 0
    for i in range(1, 200):
        Max_lenth += i*10
        if Max_lenth >= int(Max):
            break
    print(Max_lenth)
    exp1 = (int(profile.exp1)/Max_lenth) * 100
    exp2 = (int(profile.exp2)/Max_lenth) * 100
    exp3 = (int(profile.exp3)/Max_lenth) * 100

    return render(request,'profile.html',{
        'result' : "success",
        'name': profile.name,
        'account': profile.account,
        'sex': profile.sex,
        'birth': profile.birth,
        'intro': profile.intro,
        'level': level,
        'exp1': exp1,
        'exp2': exp2,
        'exp3': exp3,
        # 'balance': profile.balance,
        'character_name': profile.character_name,
        'profile_photo': profile.profile_photo,
        # 'mission_doing_chatroom_ID': ast.literal_eval(profile.mission_doing_chatroom_ID),
        # 'mission_done_chatroom_ID': ast.literal_eval(profile.mission_done_chatroom_ID),
        # 'friend_ID': ast.literal_eval(profile.friend_ID),
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

def get_img(request):
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

        group_search_all = Mission_group.objects.filter(chatroom_ID=chatroom_ID)
        group_search = group_search_all[0]

        profile_search_all = Profile.objects.filter(account=account)
        profile_search = profile_search_all[0]
        mission_doing_chatroom_ID = ast.literal_eval(profile_search.mission_doing_chatroom_ID)
        
        mission_group_check = 1
        for ID in mission_doing_chatroom_ID:
            if mission_ID == ID:
                mission_group_check = 0
                break

        if mission_group_check:
            if group_search.status == "acceptable":
                ### 修改 mission group
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
                mission_doing_chatroom_ID.append(chatroom_ID)
                profile_search_all.update(mission_doing_chatroom_ID = mission_doing_chatroom_ID)
                
                result = "success"
            elif group_search.status == "full":
                result = "group_full"
        else:
            result = "group_repeat"

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
        lastest_chatroom_ID = str(int(Mission_group.objects.order_by('pk').last().chatroom_ID) + 1)
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
            'chatroom_ID' : lastest_chatroom_ID,
        })

def submit_mission_group_check(request):
    if request.method == 'POST':
        chatroom_ID = request.POST.get("chatroom_ID")

        mission_group = Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0]
        member_ID = ast.literal_eval(mission_group.member_ID)
        status = mission_group.status
        group_name = mission_group.group_name
        mission_imformation = Mission_imformation.objects.filter(mission_ID=mission_group.mission_ID)[0]
        group_required = mission_imformation.group_required
        mission_name = mission_imformation.mission_name

        member_name = []
        for member in member_ID:
            member_name.append(Profile.objects.filter(account=member)[0].name)

        print(mission_name, member_ID, status, group_required, member_name)
        if status == "acceptable" or status == "full":
            if len(member_ID) >= int(group_required):
                return JsonResponse({
                    'result' : "success",
                    'mission_name' : mission_name,
                    'group_name' : group_name,
                    'member_ID' : member_ID,
                    'member_name' : member_name,
                })
            else:
                return JsonResponse({
                    'result' : "not_enough",
                })
        else:
            return JsonResponse({
                'result' : "error",
            })

def submit_mission_group(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        chatroom_ID = request.POST.get('chatroom_ID')

        with open('media/mission_submit_upload/' + chatroom_ID +'.jpg', 'wb') as f:
            for line in image:
                f.write(line)

        ### 修改 Mission group
        group_search_all = Mission_group.objects.filter(chatroom_ID=chatroom_ID)
        group_search_all.update(status="checking")

        ### 修改 Profile
        member_ID = ast.literal_eval(group_search_all[0].member_ID)

        for member in member_ID:
            profile_search_all = Profile.objects.filter(account=member)
            profile_search = profile_search_all[0]
            mission_doing_chatroom_ID = ast.literal_eval(profile_search.mission_doing_chatroom_ID)
            mission_done_chatroom_ID = ast.literal_eval(profile_search.mission_done_chatroom_ID)

            check_mission_doing = 0
            for ID in mission_doing_chatroom_ID:
                if chatroom_ID == ID:
                    check_mission_doing = 1
                    break 

            if check_mission_doing:
                mission_doing_chatroom_ID.remove(chatroom_ID)
                profile_search_all.update(mission_doing_chatroom_ID = mission_doing_chatroom_ID)
                mission_done_chatroom_ID.append(chatroom_ID)
                profile_search_all.update(mission_done_chatroom_ID = mission_done_chatroom_ID)

        ### create Mission submission
        mission_ID = group_search_all[0].mission_ID
        mission_name = group_search_all[0].mission_name
        group_name = group_search_all[0].group_name
        submission_pic = 'media/mission_submit_upload/' + chatroom_ID +'.jpg'
        check_status = "checking"
        check_preson = "none"
        Mission_submission.objects.create(mission_ID=mission_ID, mission_name=mission_name, chatroom_ID=chatroom_ID, group_name=group_name,
                                member_ID=member_ID, submission_pic=submission_pic, check_status=check_status, check_preson=check_preson
        )

        ### 取得刷新頁面資料
        ### ToDo ###

        return JsonResponse({
            'result' : "success",
        })



def get_mission_chatroom_list(request):
    if request.method == 'POST':
        account = request.POST.get("account")
        last_chatroom_list = request.POST.get("last_chatroom_list")
        last_chatroom_list = ast.literal_eval( '[' + last_chatroom_list + ']') 
        profile_search_all = Profile.objects.filter(account=account)
        profile_search = profile_search_all[0]
        mission_doing_chatroom_ID = ast.literal_eval(profile_search.mission_doing_chatroom_ID)
        mission_done_chatroom_ID = ast.literal_eval(profile_search.mission_done_chatroom_ID)
        mission_do_chatroom_ID = mission_doing_chatroom_ID + mission_done_chatroom_ID

        chatroom_ID_all, mission_ID, mission_name, chat_img, group_name, group_number, status, message, time = [], [], [], [], [], [], [], [], []
        count = 0
        for chatroom_ID in mission_do_chatroom_ID:
            chatroom_ID_all.append(chatroom_ID)

            group_search = Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0]
            mission_ID.append(group_search.mission_ID)
            mission_name.append(group_search.mission_name)
            chat_img.append( Mission_imformation.objects.filter(mission_ID=group_search.mission_ID)[0].mission_pic )
            group_name.append(group_search.group_name)
            group_number.append( len(ast.literal_eval(group_search.member_ID)) )
            status.append(group_search.status)

            lastest_message = Mission_Chatroom.objects.filter(chatroom_ID=chatroom_ID).order_by('pk').last()

            if lastest_message:
                message.append(lastest_message.message)
                time.append(lastest_message.time)
                # print(lastest_message.time)
            else:
                message.append("")
                time.append(datetime(1999, 3, 26, 0, 0, 0, count, tzinfo=timezone.utc))
                count += 1

        # print(chatroom_ID_all, mission_ID, mission_name, group_name, status, message, time)

        friend_chatroom_ID = ast.literal_eval(profile_search.friend_chatroom_ID)
        # print(friend_chatroom_ID)
        for chatroom_ID in friend_chatroom_ID:
            chatroom_ID_all.append(chatroom_ID)

            mission_ID.append('none')
            mission_name.append('none')
            

            sender_ID = Friend_Chatroom.objects.filter(chatroom_ID=chatroom_ID)[0].sender_ID
            reciever_ID = Friend_Chatroom.objects.filter(chatroom_ID=chatroom_ID)[0].receiver_ID
            if sender_ID == account:
                group_name_ID = reciever_ID
            elif reciever_ID == account:
                group_name_ID = sender_ID

            chat_img.append( Profile.objects.filter(account=group_name_ID)[0].profile_photo )

            group_name.append(Profile.objects.filter(account=group_name_ID)[0].name)
            group_number.append("none")
            status.append("friend")

            lastest_message = Friend_Chatroom.objects.filter(chatroom_ID=chatroom_ID).order_by('pk').last()

            if lastest_message:
                message.append(lastest_message.message)
                time.append(lastest_message.time)
                # print(lastest_message.time)
            else:
                message.append("")
                time.append(datetime(1999, 3, 26, 0, 0, 0, count, tzinfo=timezone.utc))
                count += 1

        time_copy = time.copy()

        time, chatroom_ID_all = (list(t) for t in zip(*sorted(zip(time_copy, chatroom_ID_all), reverse=True  )))
        time, mission_ID = (list(t) for t in zip(*sorted(zip(time_copy, mission_ID), reverse=True  )))
        time, mission_name = (list(t) for t in zip(*sorted(zip(time_copy, mission_name), reverse=True  )))
        time, chat_img = (list(t) for t in zip(*sorted(zip(time_copy, chat_img), reverse=True  )))
        time, group_name = (list(t) for t in zip(*sorted(zip(time_copy, group_name), reverse=True  )))
        time, group_number = (list(t) for t in zip(*sorted(zip(time_copy, group_number), reverse=True  )))
        time, status = (list(t) for t in zip(*sorted(zip(time_copy, status), reverse=True  )))
        time, message = (list(t) for t in zip(*sorted(zip(time_copy, message), reverse=True  )))

        # print(chatroom_ID_all, mission_ID, mission_name, group_name, status, message, time)
        last_chatroom_list = [str(x) for x in last_chatroom_list]

        if last_chatroom_list == chatroom_ID_all:
            return JsonResponse({
                'result' : "same",
            })
        else:
            return JsonResponse({
                'result' : "success",
                "chatroom_ID": chatroom_ID_all, "mission_ID": mission_ID, "mission_name": mission_name, "chat_img": chat_img,
                "group_name": group_name, "group_number": group_number, "status": status, "message": message, "time": time
            })

def mission_chatroom_update(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == "Send":
            chatroom_ID = request.POST.get('chatroom_ID')
            sender_ID = request.POST.get('sender_ID')
            message = request.POST.get('message')


            Mission_Chatroom.objects.create(chatroom_ID=chatroom_ID, sender_ID=sender_ID,  message=message)
            return JsonResponse({
                'result' : "success"
            })

        elif post_type == "Receive":            
            chatroom_ID = request.POST.get('chatroom_ID')
            last_sender_name_len = request.POST.get('last_sender_name_len')
            history = core_serializers.serialize("json", Mission_Chatroom.objects.filter(chatroom_ID=chatroom_ID).order_by("time"))

            group_name = Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0].group_name
            group_number = len(ast.literal_eval(Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0].member_ID))

            sender_photo, sender_name=[], []
            for mission_chatroom in Mission_Chatroom.objects.filter(chatroom_ID=chatroom_ID).order_by("time"):
                if mission_chatroom.sender_ID != "developers":
                    sender_photo.append(Profile.objects.filter(account=mission_chatroom.sender_ID)[0].profile_photo)
                    sender_name.append(Profile.objects.filter(account=mission_chatroom.sender_ID)[0].name)
                else:
                    sender_photo.append("media/profile_img/developers.jpg")
                    sender_name.append("官方訊息")
            
            if last_sender_name_len == str(len(sender_name)):
                return JsonResponse({
                    'result' : "same",
                })
            else:
                return JsonResponse({
                    'result' : "success",
                    'history' : history,
                    'group_name': group_name,
                    'group_number': group_number,
                    'sender_photo': sender_photo,
                    'sender_name': sender_name,
                })

def friend_chatroom_update(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == "Send":
            chatroom_ID = request.POST.get('chatroom_ID')
            account = request.POST.get('sender_ID')
            message = request.POST.get('message')

            sender_ID = Friend_Chatroom.objects.filter(chatroom_ID=chatroom_ID)[0].sender_ID
            reciever_ID = Friend_Chatroom.objects.filter(chatroom_ID=chatroom_ID)[0].receiver_ID
            if sender_ID == account:
                group_name_ID = reciever_ID
            elif reciever_ID == account:
                group_name_ID = sender_ID

            Friend_Chatroom.objects.create(chatroom_ID=chatroom_ID, sender_ID=account, receiver_ID=group_name_ID,  message=message)
            return JsonResponse({
                'result' : "success"
            })

        elif post_type == "Receive":            
            chatroom_ID = request.POST.get('chatroom_ID')
            last_sender_name_len = request.POST.get('last_sender_name_len')
            account = request.POST.get('account')
            history = core_serializers.serialize("json", Friend_Chatroom.objects.filter(chatroom_ID=chatroom_ID).order_by("time"))

            sender_ID = Friend_Chatroom.objects.filter(chatroom_ID=chatroom_ID)[0].sender_ID
            reciever_ID = Friend_Chatroom.objects.filter(chatroom_ID=chatroom_ID)[0].receiver_ID
            if sender_ID == account:
                group_name_ID = reciever_ID
            elif reciever_ID == account:
                group_name_ID = sender_ID

            group_name = Profile.objects.filter(account=group_name_ID)[0].name

            sender_photo, sender_name=[], []
            for friend_chatroom in Friend_Chatroom.objects.filter(chatroom_ID=chatroom_ID).order_by("time"):
                # if friend_chatroom.sender_ID != "developers":
                sender_photo.append(Profile.objects.filter(account=friend_chatroom.sender_ID)[0].profile_photo)
                # else:
                    # sender_photo.append("media/profile_img/developers.jpg")
                sender_name.append( Profile.objects.filter(account=friend_chatroom.sender_ID)[0].name )

            if last_sender_name_len == str(len(sender_name)):
                return JsonResponse({
                    'result' : "same",
                })
            else:
                return JsonResponse({
                    'result' : "success",
                    'history' : history,
                    'group_name': group_name,
                    'sender_photo': sender_photo,
                    'sender_name': sender_name,
                })


def get_mission_chatroom_member(request):
    if request.method == 'POST':
        chatroom_ID = request.POST.get('chatroom_ID')
        member_ID = ast.literal_eval(Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0].member_ID)
        leader_ID = Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0].leader_ID
        status = Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0].status

        member_name = []
        for member in member_ID:
            member_name.append(Profile.objects.filter(account=member)[0].name)

        return JsonResponse({
            'result' : "success",
            'member_ID' : member_ID,
            'leader_ID' : leader_ID,
            'member_name' : member_name,
            'status' : status,
        })

def kick_mission_chatroom_member(request):
    if request.method == 'POST':
        kicked_ID = request.POST.get("kicked_ID")
        user_ID = request.POST.get('user_ID')
        chatroom_ID = request.POST.get('chatroom_ID')

        ### 確認是否為該group leader
        if user_ID == Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0].leader_ID:

            group_search_all = Mission_group.objects.filter(chatroom_ID=chatroom_ID)
            group_search = group_search_all[0]

            member_ID = ast.literal_eval(group_search.member_ID)
            check_member = 0
            for member in member_ID:
                if kicked_ID == member:
                    check_member = 1
                    break 

            if check_member:
                ### 修改 mission group
                member_ID.remove(kicked_ID)
                group_search_all.update(member_ID = member_ID)

                if group_search.status == "full":
                    group_search_all.update(status = "acceptable")
            
                ### 修改 mission imformation
                mission_ID = group_search.mission_ID
                mission_search_all = Mission_imformation.objects.filter(mission_ID=mission_ID)
                mission_search = mission_search_all[0]
                joined = mission_search.joined
                joined = int(joined) - 1
                mission_search_all.update(joined = joined)

                joined_ID = ast.literal_eval(mission_search.joined_ID)
                joined_ID_reverse = joined_ID.copy()
                joined_ID_reverse.reverse()
                
                check_joined_ID = 0
                for ID in joined_ID_reverse:
                    if kicked_ID == ID:
                        check_joined_ID = 1
                        break 

                if check_joined_ID:
                    joined_ID_reverse.remove(kicked_ID)
                    joined_ID = joined_ID_reverse
                    joined_ID.reverse()
                    mission_search_all.update(joined_ID = joined_ID)

                ### 修改 Profile
                profile_search_all = Profile.objects.filter(account=kicked_ID)
                profile_search = profile_search_all[0]
                mission_doing_chatroom_ID = ast.literal_eval(profile_search.mission_doing_chatroom_ID)

                check_mission_doing = 0
                for ID in mission_doing_chatroom_ID:
                    if chatroom_ID == ID:
                        check_mission_doing = 1
                        break 

                if check_mission_doing:
                    mission_doing_chatroom_ID.remove(chatroom_ID)
                    profile_search_all.update(mission_doing_chatroom_ID = mission_doing_chatroom_ID)
                print(member_ID, joined, joined_ID, mission_doing_chatroom_ID)
            
            return JsonResponse({
                'result' : "success",
            })

        else:
            return JsonResponse({
                'result' : "not_leader"
            })

def manager_page(request):
    mission_submission = Mission_submission.objects.filter(check_status="checking")
    mission_submission = core_serializers.serialize("json", mission_submission)
    mission_submission = json.loads(mission_submission)

    # mission_ID, mission_name, chatroom_ID, group_name, member_ID, submission_pic, check_status, check_preson, time = [], [], [], [], [], [], [], [], []
    # for mission in mission_submission:
    #     mission_ID.append(mission.mission_ID)
    #     mission_name.append(mission.mission_name)
    #     chatroom_ID.append(mission.chatroom_ID)
    #     group_name.append(mission.group_name)
    #     member_ID.append(ast.literal_eval(mission.member_ID))
    #     submission_pic.append(mission.submission_pic)
    #     check_status.append(mission.check_status)
    #     check_preson.append(mission.check_preson)
    #     time.append(mission.time)
    # print(mission_ID, mission_name, chatroom_ID, group_name, member_ID, submission_pic, check_status, check_preson, time)
    # print(len(mission_ID))

    return render(request, 'manager.html', {
        # "mission_ID": mission_ID, "mission_name": mission_name, "chatroom_ID": chatroom_ID,
        # "group_name": group_name, "member_ID": member_ID, "submission_pic": submission_pic,
        # "check_status": check_status, "check_preson": check_preson, "time": time, "range": range(len(mission_ID)),
        "mission_submission" : mission_submission
    })

def submission_to_finish(request):
    if request.method == 'POST':
        chatroom_ID = request.POST.get('chatroom_ID')
        check_person = request.POST.get('check_person')

        ### 修改 mission submission
        mission_submission = Mission_submission.objects.filter(chatroom_ID=chatroom_ID)
        mission_submission.update(check_status="finished")
        mission_submission.update(check_preson=check_person)

        ### 修改 mission group status
        Mission_group.objects.filter(chatroom_ID=chatroom_ID).update(status="finished")

        ### 取得完成任務經驗獎勵資訊
        mission_ID = Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0].mission_ID
        mission_imformation = Mission_imformation.objects.filter(mission_ID = mission_ID)[0]

        exp1 = int(mission_imformation.exp1)
        exp2 = int(mission_imformation.exp2)
        exp3 = int(mission_imformation.exp3)
        reward = int(mission_imformation.reward)
        
        ### 修改 profile
        member_ID = ast.literal_eval(Mission_group.objects.filter(chatroom_ID=chatroom_ID)[0].member_ID)
        for member in member_ID:
            profile_all = Profile.objects.filter(account=member)
            profile = profile_all[0]
            my_exp1 = int(profile.exp1) + exp1
            my_exp2 = int(profile.exp2) + exp2
            my_exp3 = int(profile.exp3) + exp3
            my_balance = int(profile.balance) + reward

            profile_all.update(exp1 = my_exp1, exp2 = my_exp2, exp3 = my_exp3, balance = my_balance)
        
        ### 群發完成審核訊息
        sender_ID = "developers"
        message = '任務:"'+ mission_imformation.mission_name + '"已審核完成，獲得:知識+' +\
                     str(exp1) + ',社交+' + str(exp2) + ',體力+' + str(exp3) + ',獎勵金+' + str(reward) + '，請至個人資訊查看!'

        Mission_Chatroom.objects.create(chatroom_ID=chatroom_ID, sender_ID=sender_ID,  message=message)

        # return render(request, 'manager.html', {
        #     'result' : "success"
        # })

        return JsonResponse({
            'result' : "success"
        })

# 
def get_my_mission(request):
    if request.method == 'POST':
        account = request.POST.get("user_ID")
        profile = Profile.objects.filter(account=account)[0]
        mission_doing_chatroom_ID = ast.literal_eval(profile.mission_doing_chatroom_ID)
        mission_done_chatroom_ID = ast.literal_eval(profile.mission_done_chatroom_ID)
        
        mission_ID,mission_name,group_name,leader_ID,status,member_ID,mission_pic,member_name_list = [], [], [], [], [], [], [], []

        for doing_chatroom_ID in mission_doing_chatroom_ID:
            mission_ID.append(Mission_group.objects.filter(chatroom_ID=doing_chatroom_ID)[0].mission_ID)
            mission_name.append(Mission_group.objects.filter(chatroom_ID=doing_chatroom_ID)[0].mission_name)
            group_name.append(Mission_group.objects.filter(chatroom_ID=doing_chatroom_ID)[0].group_name)
            leader_ID.append(Mission_group.objects.filter(chatroom_ID=doing_chatroom_ID)[0].leader_ID)
            status.append(Mission_group.objects.filter(chatroom_ID=doing_chatroom_ID)[0].status)
            # 
            member_ID.append(ast.literal_eval(Mission_group.objects.filter(chatroom_ID=doing_chatroom_ID)[0].member_ID))
            # 
            mission_pic.append(Mission_imformation.objects.filter(mission_ID=Mission_group.objects.filter(chatroom_ID=doing_chatroom_ID)[0].mission_ID)[0].mission_pic)
            member_name = []
            for member in ast.literal_eval(Mission_group.objects.filter(chatroom_ID=doing_chatroom_ID)[0].member_ID):
                member_name.append(Profile.objects.filter(account=member)[0].name)
            member_name_list.append(member_name)
        
        for done_chatroom_ID in mission_done_chatroom_ID:
            mission_ID.append(Mission_group.objects.filter(chatroom_ID=done_chatroom_ID)[0].mission_ID)
            mission_name.append(Mission_group.objects.filter(chatroom_ID=done_chatroom_ID)[0].mission_name)
            group_name.append(Mission_group.objects.filter(chatroom_ID=done_chatroom_ID)[0].group_name)
            leader_ID.append(Mission_group.objects.filter(chatroom_ID=done_chatroom_ID)[0].leader_ID)
            status.append(Mission_group.objects.filter(chatroom_ID=done_chatroom_ID)[0].status)
            # 
            member_ID.append(ast.literal_eval(Mission_group.objects.filter(chatroom_ID=done_chatroom_ID)[0].member_ID))
            # 
            mission_pic.append(Mission_imformation.objects.filter(mission_ID=Mission_group.objects.filter(chatroom_ID=done_chatroom_ID)[0].mission_ID)[0].mission_pic)
            member_name = []
            for member in ast.literal_eval(Mission_group.objects.filter(chatroom_ID=done_chatroom_ID)[0].member_ID):
                member_name.append(Profile.objects.filter(account=member)[0].name)
            member_name_list.append(member_name)
            print(status)
        return JsonResponse({
            'result' : "success",
            'mission_ID': mission_ID,
            'mission_name': mission_name,
            'group_name': group_name,
            'leader_ID' : leader_ID,
            'status': status,
            'member_ID' : member_ID,
            'mission_pic': mission_pic,
            'member_name' : member_name_list,
            'mission_doing_chatroom_ID': mission_doing_chatroom_ID,
            'mission_done_chatroom_ID': mission_done_chatroom_ID
        })

def get_profile_page(request):
    if request.method == 'POST':
        account = request.POST.get("account")
        profile = Profile.objects.filter(account=account)[0]

        exp = [int(profile.exp1), int(profile.exp2), int(profile.exp3)]
        max_index = -1
        max_num = -1
        for i in range(len(exp)):
            if exp[i] > max_num:
                max_index = i
                max_num = exp[i]

        exp = int(profile.exp1) + int(profile.exp2) + int(profile.exp3)
        level = 1
        exp_temp = exp
        for i in range(1, 200):
            exp_temp -= i*10
            if exp_temp >= 0:
                level += 1
            else:
                exp_temp += i*10
                break

        if max_index==0:
            char = "知識"
        elif max_index==1:
            char = "社會"
        elif max_index==2:
            char = "肌肉"

        if level <= 2:
            character_name = char + "0.png"
        elif level <= 4:
            character_name = char + "1.png"
        elif level <= 6:
            character_name = char + "2.png"
        elif level <= 8:
            character_name = char + "3.png"
        elif level <= 10:
            character_name = char + "4.png"
        elif level > 10:
            character_name = char + "5.png"
        print(character_name)

        mission_done_chatroom_ID = ast.literal_eval(profile.mission_done_chatroom_ID)
        # mission_done_chatroom_ID = [1,2,3,4,5,6]
        if len(mission_done_chatroom_ID) >= 4:
            random_index = random.sample(range(0, len(mission_done_chatroom_ID)), 4)
            # [random.randint(0,len(mission_done_chatroom_ID)-1) for _ in range(4)]
        else:
            random_index = random.sample(range(0, len(mission_done_chatroom_ID)), len(mission_done_chatroom_ID))
            # [random.randint(0,len(mission_done_chatroom_ID)-1) for _ in range(len(mission_done_chatroom_ID))]

        story_pic = []
        for index in random_index:
            story_pic.append('media/mission_submit_upload/' + mission_done_chatroom_ID[index] + '.jpg')
        
        while len(story_pic) < 4:
            story_pic.append('media/mission_submit_upload/none.jpg')

        print(story_pic)

        return JsonResponse({
            'result' : "success",
            # 'name': profile.name,
            # 'sex': profile.sex,
            # 'birth': profile.birth,
            # 'intro': profile.intro,
            # 'exp1': profile.exp1,
            # 'exp2': profile.exp2,
            # 'exp3': profile.exp3,
            # 'balance': profile.balance,
            'character_name': character_name,
            'profile_photo': profile.profile_photo,
            'story_pic': story_pic,
            # 'mission_doing_chatroom_ID': ast.literal_eval(profile.mission_doing_chatroom_ID),
            # 'mission_done_chatroom_ID': ast.literal_eval(profile.mission_done_chatroom_ID),
            # 'friend_ID': ast.literal_eval(profile.friend_ID),
        })

def save_profile_intro(request):
    if request.method == 'POST':
        account = request.POST.get("account")
        intro = request.POST.get("intro")
        profile = Profile.objects.filter(account=account)
        print(intro)
        
        profile.update(intro=intro)

        return JsonResponse({
            'result' : "success"
        })

def get_main_page(request):
    if request.method == 'POST':
        account = request.POST.get("account")
        profile = Profile.objects.filter(account=account)[0]

        exp = [int(profile.exp1), int(profile.exp2), int(profile.exp3)]
        max_index = -1
        max_num = -1
        for i in range(len(exp)):
            if exp[i] > max_num:
                max_index = i
                max_num = exp[i]

        exp = int(profile.exp1) + int(profile.exp2) + int(profile.exp3)
        level = 1
        exp_temp = exp
        for i in range(1, 200):
            exp_temp -= i*10
            if exp_temp >= 0:
                level += 1
            else:
                exp_temp += i*10
                break

        if max_index==0:
            char = "知識"
        elif max_index==1:
            char = "社會"
        elif max_index==2:
            char = "肌肉"

        if level <= 2:
            character_name = char + "0.png"
        elif level <= 4:
            character_name = char + "1.png"
        elif level <= 6:
            character_name = char + "2.png"
        elif level <= 8:
            character_name = char + "3.png"
        elif level <= 10:
            character_name = char + "4.png"
        elif level > 10:
            character_name = char + "5.png"

        return JsonResponse({
            'result' : "success",
            'character_name': character_name,
            'type': char,
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

