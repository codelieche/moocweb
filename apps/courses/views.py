# _*_ coding:utf-8 _*_
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse

from operation.models import UserFavorite, CourseComments
from .models import Course, CourseResource

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

        # 根据标签id获取相似的课程
        tags_ids = course.tags.values_list('id', flat=True)
        similar_courses = []
        if tags_ids:
            similar_courses = Course.objects.filter(tags__in=tags_ids).exclude(id=course_id)
            similar_courses = similar_courses.annotate(same_tags=Count('id'))\
                .order_by('-same_tags', '-add_time')[:3]

        # 是否收藏了课程 和 本机构
        has_fav_course = False
        has_fav_org = False
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id,
                                           fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org_id,
                                           fav_type=2):
                has_fav_org = True

        return render(request, 'course_detail.html',{
            'course': course,
            'similar_courses': similar_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })

class CourseInfoView(View):
    '''
    课程章节信息View
    '''
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        # 课程资源
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course_video.html',{
            'course': course,
            'all_resources': all_resources,
        })


class CourseCommentsView(View):
    '''课程评论View'''
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        # 课程资源
        all_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course_comment.html', {
            'course': course,
            'all_resources': all_resources,
        })

class AddCommentView(View):
    '''课程添加评论View'''
    def post(self, request):
        # 先判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}',
                                content_type="application/json")
        course_id = int(request.POST.get("course_id", 0))
        comment = request.POST.get("comments", "")

        if course_id > 0 and comment:
            # get是有可能抛出异常的，filter不会
            course = Course.objects.get(id=course_id)
            course_comment = CourseComments(course=course, comments=comment,
                                            user=request.user)
            course_comment.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}',
                                content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}',
                                content_type="application/json")
