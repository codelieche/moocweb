# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import  authenticate
from django.contrib.auth import login as django_login
# Create your views here.


def login(request):
    '''用户登陆'''
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            django_login(request, user)
        return render(request, 'index.html')
        pass
    elif request.method =="GET":
        return render(request, 'login.html', {})
