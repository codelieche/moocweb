# _*_ coding:utf-8 _*_
__author__ = 'YaoYong'
__date__ = '2017/2/12 上午11:13'

from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    '''注册表单Form'''
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})
