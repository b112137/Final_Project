# Generated by Django 3.0.2 on 2021-05-24 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_shop_product_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='invitation_receive',
            field=models.TextField(default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='invitation_send',
            field=models.TextField(default=[]),
            preserve_default=False,
        ),
    ]
