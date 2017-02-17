# _*_ coding:utf-8 _*_
from django.contrib import admin

from .models import Category, Course, Lesson, Video, CourseResource, Tag

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    '''课程分类ModelAdmin'''
    list_display = ['parent', 'name', 'add_time']
    search_fields = ['parent', 'name']
    list_filter = ['parent', 'add_time']

class CourseAdmin(admin.ModelAdmin):
    '''Course管理Model'''
    list_display = ['name', 'category', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'image', 'add_time']
    search_fields = ['name', 'category', 'detail', 'degree']
    list_filter = ['degree', 'add_time', 'tags']


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

class TagAdmin(admin.ModelAdmin):
    '''标签管理Model'''
    list_display = ['name', 'add_time']
    search_fields = ['name']
    list_filter = ['name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(CourseResource, CourseResourceAdmin)
admin.site.register(Tag, TagAdmin)
