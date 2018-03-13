# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .views import CourseListView


urlpatterns = [
	# 课程列表首页
	url(r'^list/$', CourseListView.as_view(), name='course_list'),


]
