from django.db import models
import ast

# Create your models here.
class Chat(models.Model):
    room = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    name = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)
    birth = models.CharField(max_length=100)
    intro = models.TextField(blank=True)
    exp1 = models.TextField()
    exp2 = models.TextField()
    exp3 = models.TextField()
    balance = models.TextField()
    character_name = models.TextField()
    profile_photo = models.TextField()
    mission_doing_chatroom_ID = models.TextField()
    mission_done_chatroom_ID = models.TextField()
    friend_ID = models.TextField()
    owned_product_ID = models.TextField()
    time = models.DateTimeField(auto_now_add=True)



# class Profile(models.Model):

