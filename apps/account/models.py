# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class UserProfile(AbstractUser):
    '''拓展用户Model'''
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女')
    )
    nick_name = models.CharField(max_length=40, verbose_name="昵称",
                                 default='')
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, default='male', max_length=10)
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png',
                              max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

@python_2_unicode_compatible
class EmailVerifyRecord(models.Model):
    '''邮箱验证Model'''
    EMAIL_SEND_TYPE = (
        ('register', '注册'),
        ('forget', '找回密码')
    )
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(max_length=10, choices=EMAIL_SEND_TYPE,
                                 verbose_name="验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

@python_2_unicode_compatible
class Banner(models.Model):
    '''首页轮播图Model'''
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to='banner/%Y/%M', verbose_name="轮播图",
                              max_length=100)
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

