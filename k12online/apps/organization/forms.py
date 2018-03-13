# -*- coding: utf-8 -*-
import re
from django import forms

from operation.models import UserRequest


class UserRequestForm(forms.ModelForm):

	class Meta:
		model = UserRequest
		fields = ['name', 'mobile', 'course_name']

	def clean_mobile(self):
		mobile = self.cleaned_data['mobile']
		re_obj = re.compile('1\d{10}')
		if re_obj.match(mobile):
			return mobile
		else:
			raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")
