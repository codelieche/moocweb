# _*_ coding:utf-8 _*_
from django.conf.urls import url

from . import views

urlpatterns = [
    #课程列表页
    url(r'list/$', views.CourseListView.as_view(), name='course_list'),
]