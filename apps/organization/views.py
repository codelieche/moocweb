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

        org_nums = all_orgs.count()
        all_citys = CityDict.objects.all()

        # 分页器
        page_num = request.GET.get('page', 1)
        p = Paginator(all_orgs, per_page=2)
        orgs = p.page(page_num)

        return render(request, 'org_list.html',{
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "page_num_list": range(1, p.num_pages+1),
        })

