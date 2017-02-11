# _*_ coding:utf-8 _*_
from django.contrib import admin

from .models import Course, Lesson, Video, CourseResource

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    '''Course管理Model'''
    list_display = ['name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'image', 'add_time']
    search_fields = ['name', 'detail', 'degree']
    list_filter = ['degree', 'add_time']


class LessonAdmin(admin.ModelAdmin):
    '''Lesson管理Model'''
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']

class VideoAdmin(admin.ModelAdmin):
    '''Video管理Model'''
    list_display = ['lesson', 'name', 'add_time']
    search_display = ['lesson', 'name']
    list_filter = ['lesson', 'add_time']

class CourseResourceAdmin(admin.ModelAdmin):
    '''课程资源管理Model'''
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'add_time']

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(CourseResource, CourseResourceAdmin)
