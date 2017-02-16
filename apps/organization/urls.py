# _*_ coding:utf-8 _*_
from django.conf.urls import url
from . import views

urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', views.OrgListView.as_view(), name='org_list'),
    url(r'add_ask', views.AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', views.OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', views.OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', views.OrgDescView.as_view(), name="org_desc"),
    url(r'^teacher/(?P<org_id>\d+)/$', views.OrgTeacherView.as_view(), name="org_teacher"),
]
