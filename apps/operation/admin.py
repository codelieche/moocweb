# _*_ coding:utf-8 _*_
from django.contrib import admin

from .models import UserAsk, CourseComments,\
UserFavorite, UserMessage, UserCourse

# Register your models here.

class UserAskAdmin(admin.ModelAdmin):
    '''用户咨询管理Model'''
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'course_name']
    list_filter = ['name', 'course_name', 'add_time']

class CourseCommentsAdmin(admin.ModelAdmin):
    '''课程评论管理Model'''
    list_display = ['comments', 'user', 'course', 'add_time']
    search_fields = ['comments', 'user', 'course']
    list_filter = ['user', 'course', 'add_time']

class UserFavoriteAdmin(admin.ModelAdmin):
    '''用户收藏管理Model'''
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_type', 'add_time']

class UserMessageAdmin(admin.ModelAdmin):
    '''用户消息管理Admin'''
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['message', 'user']
    list_filter = ['has_read', 'add_time', 'user']

class UserCourseAdmin(admin.ModelAdmin):
    '''用户课程管理Admin'''
    list_display = ['user', 'course', 'add_time']
    search_fields = ['course', 'user']
    list_filter = ['user', 'course', 'add_time']

admin.site.register(UserAsk, UserAskAdmin)
admin.site.register(CourseComments, CourseCommentsAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
