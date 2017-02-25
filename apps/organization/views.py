# _*_ coding:utf-8 _*_
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q

from courses.models import Course
from operation.models import UserFavorite

from .models import CourseOrg, CityDict, Teacher
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

        # 搜索关键词: 机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 根据机构名字、描述搜索
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) |
                Q(desc__icontains=search_keywords)
            )

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

        # 机构是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_type=2, fav_id=org_id, user=request.user):
                has_fav = True

        return render(request, 'org_detail_homepage.html',
                      {
                          'course_org': course_org,
                          'all_course': all_course,
                          'all_teachers': all_teachers,
                          'current_page': 'home',
                          'has_fav': has_fav,
                      })

class OrgCourseView(View):
    '''机构课程列表View'''
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        all_course = course_org.course_set.all()
        # 机构是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_type=2, fav_id=org_id,
                                           user=request.user):
                has_fav = True
        return render(request, 'org_detail_course.html',
                      {
                          'course_org': course_org,
                          'all_course': all_course,
                          'current_page': 'course',
                          'has_fav': has_fav
                      })

class OrgDescView(View):
    '''机构介绍View'''
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        # 机构是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_type=2, fav_id=org_id,
                                           user=request.user):
                has_fav = True
        return render(request, 'org_detail_desc.html',
                      {
                          'course_org': course_org,
                          'current_page': 'desc',
                          'has_fav': has_fav,
                      })

class OrgTeacherView(View):
    '''机构教师列表View'''
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        all_teachers = course_org.teacher_set.all()
        # 机构是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_type=2, fav_id=org_id,
                                           user=request.user):
                has_fav = True
        return render(request, 'org_detail_teachers.html',
                      {
                          'course_org': course_org,
                          'all_teachers': all_teachers,
                          'current_page': 'teacher',
                          'has_fav': has_fav,
                      })


class  AddFavView(View):
    '''添加(取消)收藏View'''
    def post(self, request):
        fav_id = int(request.POST.get('fav_id', '0'))
        fav_type = int(request.POST.get('fav_type', '0'))

        # 如果已经收藏了，再次点击就是删除收藏
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}',
                                content_type="application/json")
        else:
            exist_records = UserFavorite.objects.filter(user=request.user,
                                                        fav_id=fav_id, fav_type=fav_type)
            if exist_records:
                # 记录已经存在则取消收藏
                exist_records.delete()
                return HttpResponse('{"status": "success", "msg": "收藏"}',
                                    content_type="application/json")
            else:
                # 添加收藏记录
                if fav_id > 0 and fav_type > 0:
                    UserFavorite.objects.create(user=request.user,
                        fav_id=int(fav_id), fav_type=fav_type)
                    return HttpResponse('{"status": "success", "msg": "已收藏"}',
                                        content_type="application/json")
                else:
                    return HttpResponse('{"status": "fail", "msg": "收藏出错"}',
                                        content_type="application/json")


class TeacherListView(View):
    '''讲师列表页View'''
    def get(self, request):
        all_teacher = Teacher.objects.all()

        # 搜索关键词: 讲师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 根据讲师名字、公司、职位搜索
            all_teacher = all_teacher.filter(
                Q(name__icontains=search_keywords) |
                Q(work_company__icontains=search_keywords) |
                Q(work_position__icontains=search_keywords)
            )

        # 对讲师排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "hot":
                all_teacher = all_teacher.order_by('-click_nums')

        # 对讲师列表分页
        page_num = 1
        try:
            page_num = int(request.GET.get('page', '1'))
        except Exception:
            page_num = 1
        p = Paginator(all_teacher, 3)
        teachers = p.page(page_num)

        # 讲师排行榜
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:5]

        return render(request, 'teachers_list.html',{
            'all_teachers': teachers,
            'teacher_nums': p.count,
            'page_num_list': range(1, p.num_pages + 1),
            'sort': sort,
            'sorted_teachers': sorted_teachers,
        })

class TeacherDetialView(View):
    '''讲师详情页View'''
    def get(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)

        # 讲师的课程
        all_courses = teacher.course_set.all()

        # 讲师排行榜
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:5]

        # 教师和机构是否已经收藏
        has_teacher_faved = False
        has_org_faved = False
        # 查询是否收藏了教师
        if UserFavorite.objects.filter(user=request.user,
                                       fav_id=teacher_id, fav_type=3):
            has_teacher_faved = True

        # 查询机构是否收藏
        if UserFavorite.objects.filter(user=request.user,
                                       fav_id=teacher.org_id, fav_type=2):
            has_org_faved = True

        return render(request, 'teacher_detail.html', {
            'teacher': teacher,
            'sorted_teachers': sorted_teachers,
            'all_courses': all_courses,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved,
        })