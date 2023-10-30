from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class MxzUser(AbstractUser):
    nickname = models.CharField(max_length=32, null=True, blank=True, verbose_name='昵称')
    photo = models.CharField(max_length=128, null=True, blank=True, verbose_name='头像')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    token = models.CharField(max_length=32, verbose_name='Token')

    def __str__(self):
        return self.username
