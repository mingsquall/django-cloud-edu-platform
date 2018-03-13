# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyForm
from utils.email_sender import send_register_email


class CustomBackEnd(ModelBackend):
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username)|Q(email=username))
			if user.check_password(password): #security check for password
				return user
		except Exception as e:
			return None


class ActivateUserView(View):
	def get(self, request, activate_code):
		# verify email valid
		all_records = EmailVerifyRecord.objects.filter(code=activate_code)
		if all_records:
			for record in all_records:
				email = record.email
				user = UserProfile.objects.get(email=email)
				user.is_active = True
				user.save()
		else:
			return render(request, "active_fail.html")
		return render(request, "login.html")


class RegisterView(View):
	def get(self, request):
		register_form = RegisterForm()
		return render(request, "register.html", {'register_form':register_form})
	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user_name = request.POST.get("email", "")
			if UserProfile.objects.filter(email=user_name):
				return render(request, "login.html", {"msg":u"用户已存在,可直接登录!", "register_form": register_form})
			pass_word = request.POST.get("password", "")
			user_profile = UserProfile()
			user_profile.username = user_name
			user_profile.email = user_name
			user_profile.is_active = False
			user_profile.password = make_password(pass_word)
			user_profile.save()
			send_register_email(user_name, "Register")
			return render(request, "login.html")
		else:
			# login_form is not valid
			return render(request, "register.html", {"register_form":register_form})


class LoginView(View):
	def get(self, request):
		return render(request, "login.html", {})
	def post(self, request):
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user_name = request.POST.get("username", "")
			pass_word = request.POST.get("password", "")
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				if user.is_active:
					login(request, user)
					return render(request, "index.html")
				else:
					return render(request, "login.html", {"msg":u"用户未激活!", "login_form": login_form})
			else:
				return render(request, "login.html", {"msg":u"用户名或密码错误!", "login_form":login_form})
		else:
			# login_form is not valid
			return render(request, "login.html", {"login_form":login_form})


class ForgetPwdView(View):
	def get(self, request):
		forget_form = ForgetForm()
		return render(request, "forgetpwd.html", {'forget_form':forget_form})
	def post(self, request):
		forget_form = ForgetForm(request.POST)
		if forget_form.is_valid():
			email = request.POST.get("email")
			if not UserProfile.objects.filter(email=email):
				return render(request, "forgetpwd.html", {"msg":u"用户未注册!"})
			else:
				send_register_email(email, "Forget")
				return render(request, "send_reset_link_success.html")
		else:
			return render(request, "forgetpwd.html", {'forget_form':forget_form})


class ResetUserView(View):
	def get(self, request, activate_code):
		# verify email valid
		all_records = EmailVerifyRecord.objects.filter(code=activate_code)
		if all_records:
			for record in all_records:
				email = record.email
				return render(request, "password_reset.html", {"email":email})
		else:
			return render(request, "active_fail.html")
		return render(request, "login.html")

class ModifyPwdView(View):
	def post(self, request):
		modify_form = ModifyForm(request.POST)
		if modify_form.is_valid():
			pwd = request.POST.get("password", "")
			re_pwd = request.POST.get("re_password", "")
			email = request.POST.get("email", "")
			if pwd != re_pwd:
				return render(request, "password_reset.html", {"email":email, "msg":u"密码不一致!"})
			user = UserProfile.objects.get(email=email)
			user.password = make_password(pwd)
			user.save()
			return render(request, "login.html", {})
		else:
			email = request.POST.get("email", "")
			return render(request, "password_reset.html", {"email":email, "modify_form":modify_form})
