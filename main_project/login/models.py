from django.db import models

# Create your models here.
class Chat(models.Model):
    room = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
