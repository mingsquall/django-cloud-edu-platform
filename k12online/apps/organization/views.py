# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import School, CityDict, Teacher
from .forms import UserRequestForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from courses.models import School
from operation.models import UserFavorite
from utils.fav_judger import fav_judge

# Create your views here.

class OrgView(View):
	"""
	明星学校列表
	"""
	def get(self, request):
		# 机构
		all_orgs = School.objects.all()
		hot_orgs = all_orgs.order_by("-click_nums")[:3]

		# 城市
		all_citys = CityDict.objects.all()

		# 城市筛选
		city_id = request.GET.get("city", "")
		if city_id:
			all_orgs = all_orgs.filter(city_id=int(city_id))

		# 类别筛选
		category = request.GET.get("ct", "")
		if category:
			all_orgs = all_orgs.filter(category=category)

		# 排序
		# get the sort request
		sort = request.GET.get("sort", "")
		if sort:
			if sort == "students":
				all_orgs = all_orgs.order_by("-student_nums")
			elif sort == "courses":
				all_orgs = all_orgs.order_by("-course_nums")

		# 计数
		org_nums = all_orgs.count()

		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_orgs, 5, request=request)
		orgs = p.page(page)

		return render(request, "org-list.html", {
			"all_orgs":orgs,
			"all_citys":all_citys,
			"org_nums":org_nums,
			"city_id":city_id,
			"category":category,
			"hot_orgs":hot_orgs,
			"sort":sort,
		})


class AddUserRequestView(View):
	"""
	用户添加咨询
	"""
	def post(self, request):
		user_request_form = UserRequestForm(request.POST)
		if user_request_form.is_valid():
			# save model to database
			user_request = user_request_form.save(commit=True)
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail", "msg":"输入有误!"}', content_type='application/json')


class OrgHomeView(View):
	"""
	机构首页
	"""
	def get(self, request, org_id):
		school = School.objects.get(id=int(org_id))
		current_page = "home"

		has_fav = fav_judge(request, school, fav_type=2)

		# filter the FK course
		all_courses = school.course_set.all()[:3]
		all_teachers = school.teacher_set.all()[:1]
		return render(request, 'org-detail-homepage.html', {
			'all_courses':all_courses,
			'all_teachers':all_teachers,
			'school':school,
			'current_page':current_page,
			'has_fav':has_fav,
		})


class OrgCourseView(View):
	"""
	学校课程列表页面
	"""
	def get(self, request, org_id):
		current_page = "course"
		school = School.objects.get(id=int(org_id))
		has_fav = fav_judge(request, school, fav_type=2)
		# filter the FK course
		all_courses = school.course_set.all()
		return render(request, 'org-detail-course.html', {
			'all_courses':all_courses,
			'school':school,
			'current_page':current_page,
			'has_fav':has_fav,
		})


class OrgDescView(View):
	"""
	学校介绍页面
	"""
	def get(self, request, org_id):
		current_page = "desc"
		school = School.objects.get(id=int(org_id))
		has_fav = fav_judge(request, school, fav_type=2)
		return render(request, 'org-detail-desc.html', {
			'school':school,
			'current_page':current_page,
			'has_fav':has_fav,
		})


class OrgTeacherView(View):
	"""
	学校讲师列表页面
	"""
	def get(self, request, org_id):
		current_page = "teacher"
		school = School.objects.get(id=int(org_id))
		has_fav = fav_judge(request, school, fav_type=2)
		# filter the FK course
		all_teachers = school.teacher_set.all()
		return render(request, 'org-detail-teachers.html', {
			'all_teachers':all_teachers,
			'school':school,
			'current_page':current_page,
			'has_fav':has_fav,
		})


class AddFavView(View):
	"""
	用户收藏/取消收藏
	"""
	def post(self, request):
		fav_id = request.POST.get('fav_id', 0)
		fav_type = request.POST.get('fav_type', 0)

		if not request.user.is_authenticated():
			# 判断用户登录状态
			return HttpResponse('{"status":"fail", "msg":"请先登录"}', content_type='application/json')
		exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
		if exist_records:
			# 如果记录存在，则表示用户取消收藏
			exist_records.delete()
			return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
		else:
			# 记录不存在，则添加一条
			user_fav = UserFavorite()
			if int(fav_id) > 0 and int(fav_type) > 0:
				user_fav.user = request.user
				user_fav.fav_id = int(fav_id)
				user_fav.fav_type = int(fav_type)
				user_fav.save()
				return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
			else:
				return HttpResponse('{"status":"fail", "msg":"收藏出错!"}', content_type='application/json')


