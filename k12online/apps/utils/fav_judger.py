# -*- coding: utf-8 -*-
from operation.models import UserFavorite

def fav_judge(request, school, fav_type):
	has_fav = False
	if request.user.is_authenticated():
		if UserFavorite.objects.filter(user=request.user, fav_id=int(school.id), fav_type=int(fav_type)):  # 2: school
			has_fav = True
	return has_fav
