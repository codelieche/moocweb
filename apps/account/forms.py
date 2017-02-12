# _*_ coding:utf-8 _*_
__author__ = 'YaoYong'
__date__ = '2017/2/12 上午11:13'

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)

