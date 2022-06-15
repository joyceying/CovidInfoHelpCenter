from django.db import models

# Create your models here.

class User(models.Model):
    """ 普通用户表 """
    name = models.CharField(verbose_name="username", max_length=16)
    password = models.CharField(verbose_name="password", max_length=64)