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
    email = models.TextField()
    intro = models.TextField(blank=True)
    exp1 = models.TextField()
    exp2 = models.TextField()
    exp3 = models.TextField()
    balance = models.TextField()
    character_name = models.TextField()
    profile_photo = models.TextField()
    mission_doing_chatroom_ID = models.TextField() #List
    mission_done_chatroom_ID = models.TextField() #List
    friend_ID = models.TextField() #List
    owned_product_ID = models.TextField() #List
    time = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.account

    def __str__(self):
        ID = self.account
        name = self.name
        concat = ID + " " + name
        return concat


class Mission_Chatroom(models.Model):
    chatroom_ID = models.CharField(max_length=100)
    sender_ID = models.CharField(max_length=100)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Friend_Chatroom(models.Model):
    sender_ID = models.CharField(max_length=100)
    receiver_ID = models.CharField(max_length=100)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Mission_imformation(models.Model):
    mission_ID = models.CharField(max_length=100)
    mission_name = models.TextField()
    launcher = models.TextField()
    mission_type = models.CharField(max_length=100)
    mission_intro = models.TextField()
    mission_pic = models.TextField()
    joined = models.TextField()
    group_required = models.TextField()
    exp1 = models.TextField()
    exp2 = models.TextField()
    exp3 = models.TextField()
    reward = models.TextField()
    joined_ID = models.TextField() #List

    def __str__(self):
        ID = self.mission_ID
        name = self.mission_name
        concat = ID + " " + name
        return concat

class Mission_group(models.Model):
    chatroom_ID = models.CharField(max_length=100)
    mission_ID = models.CharField(max_length=100)
    mission_name = models.TextField()
    group_name = models.TextField()
    group_most = models.TextField()
    leader_ID = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    member_ID = models.TextField() #List

class Shop(models.Model):
    product_ID = models.CharField(max_length=100)
    product_name = models.TextField()
    product_detail = models.TextField()
    product_price = models.TextField()
    product_left = models.TextField()

# class Profile(models.Model):

