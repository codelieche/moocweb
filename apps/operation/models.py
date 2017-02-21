# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from account.models import UserProfile
from courses.models import Course

# Create your models here.


@python_2_unicode_compatible
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

@python_2_unicode_compatible
class CourseComments(models.Model):
    '''课程评论Model'''
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    comments = models.CharField(max_length=200, verbose_name="评论")
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comments

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

@python_2_unicode_compatible
class UserFavorite(models.Model):
    '''用户收藏Model'''
    FAV_TYPE_CHOICES = (
        (1, "课程"),
        (2, "课程机构"),
        (3, "讲师")
    )
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    fav_id = models.IntegerField(default=0, verbose_name="数字ID")
    fav_type = models.IntegerField(choices=FAV_TYPE_CHOICES, default=1,
                                   verbose_name="收藏类型")
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s: %s->%s" % (self.user.username, self.fav_id, self.fav_type)

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

@python_2_unicode_compatible
class UserMessage(models.Model):
    '''用户消息Model'''
    user = models.IntegerField(default=0, verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

@python_2_unicode_compatible
class UserCourse(models.Model):
    '''用户学习课程Model'''
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0}: {1}'.format(self.user.nick_name, self.course.name)

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name
