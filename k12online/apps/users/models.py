# -*- encoding: utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
	GENDER_CHOICES = (
		("Male", u"男"),
		("Female", u"女"),
	)
	nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default=u"")
	birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
	gender = models.CharField(choices=GENDER_CHOICES, default="female", max_length=6)
	address = models.CharField(max_length=100, default=u"")
	mobile = models.CharField(max_length=11, null=True, blank=True)
	image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

	class Meta:
		verbose_name = "用户信息"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.username

class EmailVerifyRecord(models.Model):
	SEND_CHOICES = (
		("Register", u"注册"),
		("Forget", u"找回密码")
	)
	code = models.CharField(max_length=20, verbose_name=u"验证码")
	email = models.EmailField(max_length=50, verbose_name=u"邮箱")
	send_type = models.CharField(choices=SEND_CHOICES, max_length=10, verbose_name=u"验证码类型")
	send_time = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")

	class Meta:
		verbose_name = u"邮箱验证码"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return '{0} ({1})'.format(self.code, self.email)

class Banner(models.Model):
	title = models.CharField(max_length=100, verbose_name=u"标题")
	image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
	url = models.URLField(max_length=200, verbose_name=u"访问地址")
	index = models.IntegerField(default=100, verbose_name=u"顺序")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"轮播图"
		verbose_name_plural = verbose_name
