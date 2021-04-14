from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.views.generic import View
import json
from login.models import Chat
from rest_framework import serializers
from django.core import serializers as core_serializers

# Create your views here.
def login_page(request):
    time = datetime.now()
    return render(request, 'login.html', {
        'datetime': time
    })

def chat_update(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == "Send":
            room = request.POST.get('room')
            user = request.POST.get('user')
            content = request.POST.get('content')
            print(content)
            with open('msg.txt', 'a') as msg_file:
                msg_file.write( content+'\n' )
                msg_file.close()

            Chat.objects.create(room=room, user=user,  content=content)
            return JsonResponse({
                'result' : "success"
            })

        elif post_type == "Receive":
            room = request.POST.get('room')

            history = []
            with open('msg.txt', 'r') as msg_file:
                line = msg_file.readline()
                while line:
                    history.append(line)
                    line = msg_file.readline()
                msg_file.close()

            # room_history = core_serializers.serialize("json", Chat.objects.all())
            room_history = core_serializers.serialize("json", Chat.objects.filter(room=room).order_by("time"))
            # print(room_history)

            return JsonResponse({
                'result' : "success",
                'msg' : history,
                'room_history' : room_history,
            })

