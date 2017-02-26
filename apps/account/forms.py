# _*_ coding:utf-8 _*_
__author__ = 'YaoYong'
__date__ = '2017/2/12 上午11:13'

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    '''注册表单Form'''
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ForgetPasswordForm(forms.Form):
    '''忘记密码Form'''
    email = forms.EmailField(max_length=50, required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})

class ModifyPasswordForm(forms.Form):
    '''修改密码Form'''
    # email = forms.EmailField(max_length=50, required=True)
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

class UploadImageForm(forms.ModelForm):
    '''上传图片图片form'''
    class Meta:
        model = UserProfile
        fields = ['image']

class UserInfoForm(forms.ModelForm):
    '''个人中心修改用户信息form'''
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']