# Generated by Django 3.0.2 on 2021-05-05 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20210505_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend_chatroom',
            name='message',
            field=models.TextField(blank=True),
        ),
    ]