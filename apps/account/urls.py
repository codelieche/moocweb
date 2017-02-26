# _*_ coding:utf-8 _*_

from django.conf.urls import url

from . import views
from .models import UserProfile

urlpatterns = [
    url('^home/$', views.UserInfoView.as_view(), name='home'),
]
