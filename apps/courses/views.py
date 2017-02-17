# _*_ coding:utf-8 _*_
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.core.paginator import Paginator
from .models import Course

# Create your views here.


class CourseListView(View):
    '''
    课程列表页View
    '''
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        # 对课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_orgs = all_courses.order_by("-click_nums")

        # 对课程列表进行分页
        page_num = 1
        try:
            page_num = int(request.GET.get('page', '1'))
        except Exception:
            # 如果传来的page是个字符，就不能转成int
            page_num = 1
        p = Paginator(all_courses, 3)
        courses = p.page(page_num)

        # 热门课程
        hot_courses = all_courses.order_by('-click_nums')[:3]

        return render(request, 'course_list.html',{
            'all_courses': courses,
            "page_num_list": range(1, p.num_pages + 1),
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    '''
    课程详情页View
    '''
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        course.click_nums += 1
        course.save(update_fields=['click_nums'])
        return render(request, 'course_detail.html',{
            'course': course,
        })