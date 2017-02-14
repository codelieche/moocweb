# _*_ coding:utf-8 _*_
from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import mask_hash

from utils.email_send import send_register_email
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm


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
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # 对user是否激活进行判断
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': "用户还没激活"})
            return render(request, 'login.html', {"msg": "用户名或者密码错误"})
        else:
            return render(request, 'login.html', {"login_form": login_form})

def user_logout(request):
    logout(request)
    return render(request, 'login.html')

class RegisterView(View):
    '''用户注册View'''
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            ## 需要判断email是否存在
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html',
                              {'register_form': register_form,
                               'msg': 'Email已经注册，请更换'})

            pass_word = register_form.cleaned_data['password']
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = mask_hash(pass_word)
            # user_profile.set_password(pass_word)
            # 点击邮箱中的激活链接，is_active才变成True
            user_profile.is_active = False
            user_profile.save()

            # 发送验证邮件
            send_register_email(email, "register")
            # login(request, user_profile)
            return render(request, 'login.html')

        else:
            return render(request, 'register.html', {'register_form': register_form})

class ActiveUserView(View):
    '''用户激活View'''
    def get(self, request, active_code):
        # 查询记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)

                # 激活并登陆账号
                user.is_active = True
                user.save()
                ## 这里还需要控制 再次点击active的链接
                login(request, user)

                # 跳转去首页
                return redirect('index')
        else:
            # 没查询到激活链接
            # return redirect('register')
            return render(request, 'active_fail.html')