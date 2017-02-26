# _*_ coding:utf-8 _*_

from django.conf.urls import url

from . import views
from .models import UserProfile

urlpatterns = [
    # 个人中心页
    url('^home/$', views.UserInfoView.as_view(), name='home'),
    # 用户上传头像图片
    url('^image/upload/$', views.UploadImageView.as_view(), name='image_upload'),
]