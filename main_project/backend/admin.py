from django.contrib import admin
from backend.models import Profile, Mission_imformation, Mission_Chatroom, Mission_group, Mission_submission

# Register your models here.
admin.site.register(Profile)
admin.site.register(Mission_imformation)
admin.site.register(Mission_Chatroom)
admin.site.register(Mission_group)
admin.site.register(Mission_submission)