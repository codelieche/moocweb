# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View

from .models import Course

# Create your views here.


class CourseListView(View):
    '''
    课程列表页View
    '''
    def get(self, request):
        all_courses = Course.objects.all()

        return render(request, 'course_list.html',{
            'all_courses': all_courses,
        })
