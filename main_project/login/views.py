from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.views.generic import View
import json


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
            text = request.POST.get('text')
            with open('msg.txt', 'a') as msg_file:
                msg_file.write( text+'\n' )
                msg_file.close()
            return JsonResponse({
                'result' : "success"
            })

        elif post_type == "Receive":
            history = []
            with open('msg.txt', 'r') as msg_file:
                line = msg_file.readline()
                while line:
                    history.append(line)
                    line = msg_file.readline()
                msg_file.close()

            return JsonResponse({
                'result' : "success",
                'msg' : history
            })

