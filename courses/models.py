#coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class Course(models.Model):
    '''课程基本信息Model'''
    DEGREE_CHOISES = (
        ('cj', "初级"),
        ('zj', "中级"),
        ('gj', "高级")
    )
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(choices=DEGREE_CHOISES, max_length=2, default='cj',
                              verbose_name="难度")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面",
                              max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

class Lesson(models.Model):
    '''章节信息Model'''
    pass

class Video(models.Model):
    '''视频Model'''
    pass

class CourseResource(models.Model):
    '''课程资源Model'''
    pass

