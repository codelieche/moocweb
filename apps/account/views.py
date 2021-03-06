# _*_ coding:utf-8 _*_
import json
from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import mask_hash
from django.http import HttpResponse
from django.core.paginator import Paginator

from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

from operation.models import UserCourse, UserFavorite, UserMessage

from organization.models import CourseOrg, Teacher
from courses.models import Course

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPasswordForm,\
    ModifyPasswordForm, UploadImageForm, UserInfoForm


# Create your views here.


class CustomBackend(ModelBackend):
    '''自定义user后台认证'''
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # Django存储的用户密码是密文的，所以查询的时候不传递password
            ## 用Q来设置并集
            user = UserProfile.objects.get(
                Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LoginView(View):
    '''用户登陆View'''
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        '''用户登陆Post'''
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # 对user是否激活进行判断
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': "用户还没激活"})
            return render(request, 'login.html', {"msg": "用户名或者密码错误"})
        else:
            return render(request, 'login.html', {"login_form": login_form})

def user_logout(request):
    logout(request)
    return render(request, 'login.html')

class RegisterView(View):
    '''用户注册View'''
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            ## 需要判断email是否存在
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html',
                              {'register_form': register_form,
                               'msg': 'Email已经注册，请更换'})

            pass_word = register_form.cleaned_data['password']
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = mask_hash(pass_word)
            # user_profile.set_password(pass_word)
            # 点击邮箱中的激活链接，is_active才变成True
            user_profile.is_active = False
            user_profile.save()

            # 发送验证邮件
            send_register_email(email, "register")
            # login(request, user_profile)

            # 写入注册信息
            UserMessage.objects.create(user=user_profile.id,
                                       message="欢迎注册mooc在线")
            return render(request, 'login.html')

        else:
            return render(request, 'register.html', {'register_form': register_form})

class ActiveUserView(View):
    '''用户激活View'''
    def get(self, request, active_code):
        # 查询记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)

                # 激活并登陆账号
                user.is_active = True
                user.save()
                ## 这里还需要控制 再次点击active的链接
                login(request, user)

                # 跳转去首页
                return redirect('index')
        else:
            # 没查询到激活链接
            # return redirect('register')
            return render(request, 'active_fail.html')

class ForgetPasswordView(View):
    '''忘记密码View'''
    def get(self, request):
        forget_form = ForgetPasswordForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetPasswordForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.cleaned_data['email']
            # 发送忘记密码 验证邮箱
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})

class ResetPasswordView(View):
    '''重置密码View'''
    def get(self, request, reset_code):
        record = EmailVerifyRecord.objects.get(code = reset_code)
        if record:
            email = record.email
            return render(request, 'password_reset.html', {"email": email})
        else:
            return render(request, 'active_fail.html')

        return render(request, 'login.html')

class ModifyPasswordView(View):
    '''更改密码View'''
    def post(self, request):
        modify_form = ModifyPasswordForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get('email', "")
            password = modify_form.cleaned_data['password1']
            password2 = modify_form.cleaned_data['password2']
            if password == password2:
                user = UserProfile.objects.get(email=email)
                if user:
                    user.set_password(password)
                    user.save()
                    # 登陆且跳转到首页
                    # login(request, user)

                    # 写入信息：成功重置密码
                    msg = "{0}成功重置密码".format(user.nick_name)
                    UserMessage.objects.create(user=user.id, message=msg)

                    return redirect('login')
                else:
                    return render(request, 'password_reset.html',
                                  {'msg': "此email用户不存在"})
            else:
                return render(request, 'password_reset.html',
                              {'email': email, 'msg': "输入的密码不相等"})
        else:
            return render(request, 'password_reset.html',
                          {'email': request.POST.get('email', ''),
                           'msg': '请重新输入'})

class UserInfoView(LoginRequiredMixin, View):
    '''用户个人信息View'''
    # 需要登陆才可以进入用户中心
    def get(self, request):
        return render(request, 'usercenter/info.html', {

        })

    def post(self, request):
        # 是修改所以要传入instance对象
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success", "msg": "修改成功"}',
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps(user_info_form.errors),
                                content_type="application/json")

class UploadImageView(LoginRequiredMixin, View):
    '''用户修改头像图片View'''
    def post(self, request):
        # 与以前的post数据有差异哦: 需要加个request.FILES
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)

        if image_form.is_valid():
            # request.user.image = image_form.cleaned_data['image']
            # request.user.save()
            # ModelForm可以直接保存
            image_form.save()
            return HttpResponse('{"status": "success", "msg": "上传成功"}',
                                content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg": "上传失败"}',
                                content_type="application/json")

class UpdatePasswordView(View):
    '''修改密码View'''
    def post(self, request):
        modify_form = ModifyPasswordForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', "")
            pwd2 = request.POST.get('password2', "")

            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',
                                    content_type="application/json")
            user = request.user
            user.set_password(pwd1)
            user.save()

            # 写入信息：成功修改密码
            msg = "{0}成功修改密码".format(user.nick_name)
            UserMessage.objects.create(user=user.id, message=msg)

            return HttpResponse('{"status":"success","msg":"修改完成"}',
                                    content_type="application/json")

        else:
            return HttpResponse(json.dumps(modify_form.errors),
                                content_type="application/json")

class SendEmailCodeView(LoginRequiredMixin, View):
    '''发送邮箱验证码'''
    def get(self, request):
        email = request.GET.get('email', '')
        # email必须是个未注册的邮箱
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}',
                                content_type="application/json")
        else:
            # 发送update邮箱验证码
            send_register_email(email, "update_email")
            return HttpResponse('{"status":"success"}',
                                content_type="application/json")

class UpdateEmailView(LoginRequiredMixin, View):
    '''更新邮箱View'''
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code,
                                                      send_type="update_email")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}',
                                content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "email": "验证码错误"}',
                                content_type="application/json")

class MyCourseView(LoginRequiredMixin, View):
    '''
    我的课程View
    '''
    def get(self, request):
        # 取出用户的所有课程
        user_courses = UserCourse.objects.filter(user=request.user)
        # 课程列表在UserCourse对象的course字段
        user_courses = [i.course for i in user_courses]

        return render(request, 'usercenter/mycourse.html', {
            'user_courses': user_courses,
        })

class MyFavOrgView(LoginRequiredMixin, View):
    '''我的收藏:机构'''
    def get(self, request):
        # 取出用户收藏的机构名称
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        fav_orgs_ids = [i.fav_id for i in fav_orgs]
        org_list = CourseOrg.objects.filter(id__in=fav_orgs_ids)

        return render(request, 'usercenter/fav_org.html', {
            'org_list': org_list,
        })

class MyFavTeacherView(LoginRequiredMixin, View):
    '''我的收藏:Teacher'''
    def get(self, request):
        # 取出用户收藏的讲师名称
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        fav_teachers_ids = [i.fav_id for i in fav_teachers]
        teacher_list = Teacher.objects.filter(id__in=fav_teachers_ids)

        return render(request, 'usercenter/fav_teacher.html', {
            'teacher_list': teacher_list,
        })

class MyFavCourseView(LoginRequiredMixin, View):
    '''我的收藏:Course'''
    def get(self, request):
        # 取出用户收藏的课程
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        fav_courses_ids = [i.fav_id for i in fav_courses]
        course_list = Course.objects.filter(id__in=fav_courses_ids)

        return render(request, 'usercenter/fav_course.html', {
            'course_list': course_list,
        })

class MyMessageView(LoginRequiredMixin, View):
    '''我的消息View'''
    def get(self, request):
        # UserMessage的user字段是0或者user.id，0是系统消息
        all_message = UserMessage.objects.filter(user__in=[0, request.user.id]).\
            order_by('-add_time')

        # 对信息进行分页
        p = Paginator(all_message, 5)
        page_num = 1
        try:
            page_num = int(request.GET.get('page', '1'))
        except Exception:
            page_num = 1

        messages = p.page(page_num)

        return render(request, 'usercenter/message.html', {
            'messages': messages,
            'page_num_list': range(1, p.num_pages + 1),
        })