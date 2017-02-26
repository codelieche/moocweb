# _*_ coding:utf-8 _*_

from django.conf.urls import url

from . import views
from .models import UserProfile

urlpatterns = [
    # 个人中心页
    url('^home/$', views.UserInfoView.as_view(), name='home'),
    # 用户上传头像图片
    url('^image/upload/$', views.UploadImageView.as_view(), name='image_upload'),
    # 修改密码
    url('^update/pwd/', views.UpdatePasswordView.as_view(), name="update_pwd"),
    # 发送修改邮箱验证码
    url('^sendemail_code/$', views.SendEmailCodeView.as_view(), name="sendemail_code"),
    # 更新email
    url('^update/email/$', views.UpdateEmailView.as_view(), name="update_email"),

]
