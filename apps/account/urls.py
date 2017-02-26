# _*_ coding:utf-8 _*_

from django.conf.urls import url

from . import views
from .models import UserProfile

urlpatterns = [
    # 个人中心页
    url('^info/$', views.UserInfoView.as_view(), name='home'),
    # 用户上传头像图片
    url('^image/upload/$', views.UploadImageView.as_view(), name='image_upload'),
    # 修改密码
    url('^update/pwd/', views.UpdatePasswordView.as_view(), name="update_pwd"),
    # 发送修改邮箱验证码
    url('^sendemail_code/$', views.SendEmailCodeView.as_view(), name="sendemail_code"),
    # 更新email
    url('^update/email/$', views.UpdateEmailView.as_view(), name="update_email"),
    # 我的课程
    url('^mycourse/$', views.MyCourseView.as_view(), name="mycourse"),
    # 我的收藏:机构
    url('^myfav/org/$', views.MyFavOrgView.as_view(), name="my_fav_org"),
    # 我的收藏:讲师
    url('^myfav/teacher/$', views.MyFavTeacherView.as_view(), name="my_fav_teacher"),
    # 我的收藏:课程
    url('^myfav/course/$', views.MyFavCourseView.as_view(), name="my_fav_course"),
    # 用户消息
    url('^message/$', views.MyMessageView.as_view(), name="message")

]
