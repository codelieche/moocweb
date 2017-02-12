# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile

# Create your views here.

class CustomBackend(ModelBackend):
    '''自定义user后台认证'''
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # Django存储的用户密码是密文的，所以查询的时候不传递password
            ## 用Q来设置并集
            user = UserProfile.objects.get(
                Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LoginView(View):
    '''用户登陆View'''
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        '''用户登陆Post'''
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {"msg": "用户名或者密码错误"})

def user_logout(request):
    logout(request)
    return render(request, 'login.html')