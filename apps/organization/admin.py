# _*_ coding:utf-8 _*_
from django.contrib import admin

from .models import CourseOrg, Teacher, CityDict

# Register your models here.


class CourseOrgAdmin(admin.ModelAdmin):
    '''课程机构管理Model'''
    list_display = ['name', 'category', 'desc', 'address', 'city', 'add_time']
    search_fields = ['name', 'category', 'address', 'city']
    list_filter = ['name', 'category', 'address', 'city', 'add_time']

class TeacherAdmin(admin.ModelAdmin):
    '''教师管理Model'''
    list_display = ['name', 'org', 'image', 'age', 'work_years', 'work_position', 'points',
                    'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'org', 'points']
    list_filter = ['org', 'work_years', 'work_position', 'add_time']

class CityDictAdmin(admin.ModelAdmin):
    '''城市管理Model'''
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'add_time']

admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(CityDict, CityDictAdmin)
