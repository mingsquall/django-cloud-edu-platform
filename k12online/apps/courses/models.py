# -*- encoding: utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import School

# Create your models here.


class Course(models.Model):
	DEGREE_CHOICES = (
		("low", u"初级"),
		("mid", u"中级"),
		("high", u"高级"),
	)
	course_org = models.ForeignKey(School, verbose_name=u"所属学校", null=True)
	name = models.CharField(max_length=50, verbose_name=u"课程名")
	desc = models.CharField(max_length=300, verbose_name=u"课程描述")
	detail = models.TextField(verbose_name=u"课程详情")
	category = models.CharField(max_length=20, default=u"" ,verbose_name=u"课程类别")
	degree = models.CharField(choices=DEGREE_CHOICES, max_length=3, verbose_name=u"难度")
	learn_times = models.IntegerField(default=0, verbose_name=u"学习课时")
	student_nums = models.IntegerField(default=0, verbose_name=u"学习人数")
	fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
	image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
	click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"课程"
		verbose_name_plural = verbose_name

	def get_chara_nums(self):
		# 获取课程章节数
		return self.lesson_set.all().count()

	def get_learn_users(self):
		return self.usercourse_set.all()[:6]

	def __unicode__(self):
		return self.name

class Lesson(models.Model):
	course = models.ForeignKey(Course, verbose_name=u"课程")
	name = models.CharField(max_length=100, verbose_name=u"章节名")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"章节"
		verbose_name_plural = verbose_name


class Video(models.Model):
	lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
	name = models.CharField(max_length=100, verbose_name=u"视频名")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"视频"
		verbose_name_plural = verbose_name


class CourseResource(models.Model):
	course = models.ForeignKey(Course, verbose_name=u"课程")
	name = models.CharField(max_length=100, verbose_name=u"名称")
	download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"课程资源"
		verbose_name_plural = verbose_name
