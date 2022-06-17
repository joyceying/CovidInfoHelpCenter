from django.db import models


# Create your models here.

class User(models.Model):
    """ 普通用户表 """
    name = models.CharField(verbose_name="name", max_length=16)
    Email = models.EmailField(verbose_name="email", max_length=20)
    password = models.CharField(verbose_name="password", max_length=64)
    DOB = models.CharField(verbose_name="DOB", max_length=20)
    age = models.IntegerField(verbose_name="age")

    def __str__(self):
        return self.name


class reportDetail(models.Model):
    name = models.CharField(max_length=50)
    closeContact = models.CharField(max_length=100)
    symptoms = models.TextField()
    date = models.CharField(max_length=50)
    image = models.ImageField(upload_to='upload_image')
    class Meta:
        db_table ="reportdetail"





