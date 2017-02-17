#coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from utils.storage import ImageStorage
from organization.models import CourseOrg, Teacher

# Create your models here.


@python_2_unicode_compatible
class Category(models.Model):
    '''课程分类Model'''
    name = models.CharField(max_length=50, verbose_name="课程分类")
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="上级分类")
    add_time = models.DateTimeField(auto_created=True, verbose_name="添加时间")

    def __str__(self):
        if self.parent:
            return '{0}/{1}'.format(self.parent.name, self.name)
        else:
            return self.name

    class Meta:
        verbose_name = "类别"
        verbose_name_plural = verbose_name



@python_2_unicode_compatible
class Course(models.Model):
    '''课程基本信息Model'''
    DEGREE_CHOISES = (
        ('cj', "初级"),
        ('zj', "中级"),
        ('gj', "高级")
    )
    name = models.CharField(max_length=50, verbose_name='课程名')
    category = models.ForeignKey(Category, verbose_name="课程类别")
    tags = models.ManyToManyField('Tag', verbose_name="标签")
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构',
                                   null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", null=True, blank=True)
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(choices=DEGREE_CHOISES, max_length=2, default='cj',
                              verbose_name="难度")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面",
                              max_length=100, storage=ImageStorage())
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    youneed_know = models.CharField(max_length=300, verbose_name="课程须知")
    teacher_tell = models.CharField(max_length=300, verbose_name="老师告诉你")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    def get_zj_nums(self):
        '''获取课程章节数'''
        return self.lesson_set.count()

    def get_learn_users(self):
        '''获取学生数'''
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        '''获取课程章节信息'''
        return self.lesson_set.all()

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

@python_2_unicode_compatible
class Lesson(models.Model):
    '''章节信息Model'''
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return '{0}:=> {1}'.format(self.course.name, self.name)

    def get_lesson_video(self):
        '''获取章节的所有video'''
        return self.video_set.all()

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

@python_2_unicode_compatible
class Video(models.Model):
    '''视频Model'''
    lesson = models.ForeignKey(Lesson, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    url = models.CharField(max_length=200, default="", verbose_name="访问链接")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

@python_2_unicode_compatible
class CourseResource(models.Model):
    '''课程资源Model'''
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="资源文件",
                                max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class Tag(models.Model):
    '''课程标签'''
    name = models.CharField(max_length=20, verbose_name="标签", unique=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
