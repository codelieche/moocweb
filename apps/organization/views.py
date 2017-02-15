# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator

from .models import CourseOrg, CityDict
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

