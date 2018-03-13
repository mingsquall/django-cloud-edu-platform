# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .views import OrgView, AddUserRequestView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView

urlpatterns = [
	# 明星学校列表首页
	url(r'^list/$', OrgView.as_view(), name='org_list'),
	url(r'^add_request/$', AddUserRequestView.as_view(), name="add_request"),
	url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
	url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
	url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
	# 学校收藏
	url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),
]
