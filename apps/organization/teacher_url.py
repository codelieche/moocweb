# _*_ coding:utf-8 _*_

from django.conf.urls import url
from . import views

urlpatterns = [

    # 教师列表页
    url('^list/$', views.TeacherListView.as_view(), name="list"),

    # 讲师详情页
    url(r'^detail/(?P<teacher_id>\d+)/$', views.TeacherDetialView.as_view(),
        name="detail"),


]


