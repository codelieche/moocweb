#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from utils.storage import ImageStorage

# Create your models here.


@python_2_unicode_compatible
class CourseOrg(models.Model):
    '''课程机构Model'''
    CATEGORY_CHOICES = (
        ('pxjg', "培训机构"),
        ('gr', "个人"),
        ('gx', "高校")

    )
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    category = models.CharField(verbose_name="机构类别", max_length=20,
                                default="pxjg", choices=CATEGORY_CHOICES)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="封面图",
                              max_length=100, storage=ImageStorage())
    address = models.CharField(max_length=150, verbose_name="机构地址")
    city = models.ForeignKey("CityDict", verbose_name="所在城市")
    students = models.IntegerField(default=0, verbose_name="学生人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return self.name

    def get_teacher_nums(self):
        '''获取课程机构教师数'''
        return self.teacher_set.count()

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

@python_2_unicode_compatible
class Teacher(models.Model):
    '''授课教师Model'''
    org = models.ForeignKey(to="CourseOrg", verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="教师名")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像",
                              max_length=100, storage=ImageStorage())
    age = models.IntegerField(default=0, verbose_name="年龄")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="就职特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name
