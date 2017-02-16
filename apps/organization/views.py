# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from django.http import HttpResponse

from courses.models import Course

from .models import CourseOrg, CityDict
from .forms import UserAskForm

# Create your views here.


class OrgListView(View):
    '''课程机构列表View'''
    def get(self, request):
        # 先查找到所有课程机构 和 城市
        all_orgs = CourseOrg.objects.all()
        # 筛选: 城市
        city_id = request.GET.get("city", "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)
        # 筛选: 分类
        category = request.GET.get("category", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序 students courses
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 统计当前条件的org个数
        org_nums = all_orgs.count()

        all_citys = CityDict.objects.all()

        # 分页器
        page_num = request.GET.get('page', 1)
        p = Paginator(all_orgs, per_page=2)
        orgs = p.page(page_num)

        # 热门机构
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        return render(request, 'org_list.html',{
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "page_num_list": range(1, p.num_pages+1),
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            # 注意json数据需要是双引号的
            return HttpResponse('{"status": "success"}',
                                content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg": "添加出错"}',
                                content_type="application/json")

class OrgHomeView(View):
    '''机构首页View'''
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:2]
        return render(request, 'org_detail_homepage.html',
                      {
                          'course_org': course_org,
                          'all_course': all_course,
                          'all_teachers': all_teachers,
                      })

class OrgCourseView(View):
    '''机构课程列表View'''
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        all_course = course_org.course_set.all()
        return render(request, 'org_detail_course.html',
                      {
                          'course_org': course_org,
                          'all_course': all_course,
                      })