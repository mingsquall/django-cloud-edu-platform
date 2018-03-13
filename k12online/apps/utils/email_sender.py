# -*- coding: utf-8 -*-
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from k12online.settings import EMAIL_FROM


def generate_random_str(randomlength=8):
	str = ''
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str += chars[random.randint(0, length)]
	return str


def send_register_email(email, send_type="Register"):
	email_record = EmailVerifyRecord()
	code = generate_random_str(16) # activate_code
	email_record.code = code
	email_record.email = email
	email_record.send_type = send_type
	email_record.save()

	email_title = ""
	email_body = ""

	if send_type == "Register":
		email_title = u"阿凡题云课堂 邮箱验证"
		email_body = \
		u'''
		亲爱的afanti用户您好
		这是来自afanti的验证邮件。此邮件用来验证您的邮箱真实有效。
		请点击以下链接激活您的邮箱
		http://127.0.0.1:8000/active/{0}
		如果以上链接无法点击，请将上面的地址复制到您的浏览器（如IE）的地址栏

		此邮件为系统自动发送邮件，请勿回复
		'''.format(code)

		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_status:
			pass
	elif send_type == "Forget":
		email_title = u"阿凡题云课堂 密码重置"
		email_body = \
		u'''
		亲爱的afanti用户您好
		这是来自afanti的验证邮件。此邮件用来重置您的密码。
		请点击以下链接重置您的密码
		http://127.0.0.1:8000/reset/{0}
		如果以上链接无法点击，请将上面的地址复制到您的浏览器（如IE）的地址栏

		此邮件为系统自动发送邮件，请勿回复
		'''.format(code)

		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_status:
			pass



