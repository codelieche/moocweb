# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View

from .models import CourseOrg, CityDict
# Create your views here.


class OrgListView(View):
    '''课程机构列表View'''
    def get(self, request):
        # 先查找到所有课程机构 和 城市
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        all_citys = CityDict.objects.all()
        return render(request, 'org_list.html',{
            "all_orgs": all_orgs,
            "all_citys": all_citys,
            "org_nums": org_nums
        })

