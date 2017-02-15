# _*_ coding:utf-8 _*_
from django.conf.urls import url
from . import views

urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', views.OrgListView.as_view(), name='org_list'),
    url(r'add_ask', views.AddUserAskView.as_view(), name='add_ask'),
]
