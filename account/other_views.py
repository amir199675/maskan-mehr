from django.shortcuts import render, HttpResponse, Http404, redirect
from account.models import MyUser
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from debt.models import *
from django.db.models import Q
from django.contrib.auth.models import Group
from datetime import datetime



def Sidbar(user):
	select_user = user
	groups = Group.objects.all()
	try:
		user_groups = select_user.groups.all()
		for group in groups:
			for user_group in user_groups:
				if group.name == user_group.name and user_group.name == 'Manager':
					apartments = Apartment.objects.filter(manager_id=select_user)

					info = {
						'apartments':apartments,
						'status':'Manager',
					}
					return info
				elif group.name == user_group.name and user_group.name == 'Admin':
					return 'Admin'
	except:
		return 'User'



@login_required()
def Manager_Profile(request):
	select_user = request.user

	logged = Sidbar(select_user)

	if logged['status'] == 'Manager':
		apartments = logged['apartments']

	else:
		apartments = None



	try:
		last_rents = Rent.objects.filter(Q(family_id__protector=request.user) | Q(family_id__user_id=request.user),
										 Q(method='NotPaid'))
	except:
		last_rents = None

	try:
		fu_rents = Rent.objects.filter(Q(family_id__protector=request.user) | Q(family_id__user_id=request.user),
									   Q(method='Online') | Q(method='Cash'))
	except:
		fu_rents = None
	if request.method == 'POST' and 'password' in request.POST:
		old_pass = request.POST['old_password']
		password = request.POST['password']
		re_password = request.POST['re_password']
		test_pass = authenticate(username=select_user.username, password=old_pass)
		# if test_pass:
		# 	return HttpResponse(test_pass)
		# else:
		# 	return HttpResponse('fs')

		if test_pass:
			if password == re_password:
				select_user.set_password(password)
				select_user.save()
				context = {
					'success': True,
					'pass_change': True,
					'message': 'تغییر رمز با موفقیت انجام شد.',
					'fu_rents': fu_rents,
					'last_rents': last_rents,

				}
				return render(request, 'admin-panel/user/manager/profile.html', context)
			else:
				context = {
					'error': True,
					'pass_change': True,
					'message': 'لطفا رمز جدید را با دقت وارد کنید.',
					'fu_rents': fu_rents,
					'last_rents': last_rents,

				}
				return render(request, 'admin-panel/user/manager/profile.html', context)
		else:
			context = {
				'error': True,
				'pass_change': True,
				'message': 'لطفا در صحیح وارد کردن رمز عبور اولیه دقت فرمایید.',
				'fu_rents': fu_rents,
				'last_rents': last_rents,

			}
			return render(request, 'admin-panel/user/manager/profile.html', context)
	if request.method == 'POST' and 'first_name' in request.POST:
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		phone_number = request.POST['phone_number']
		email = request.POST['email']
		select_user.phone_number = phone_number
		select_user.email = email
		select_user.first_name = first_name
		select_user.last_name = last_name
		select_user.save()
		context = {
			'success': True,
			'infor': True,
			'message': 'مشخصات شما با موفقیت ثبت شد.',
			'fu_rents': fu_rents,
			'last_rents': last_rents,

		}
		return render(request, 'admin-panel/user/profile.html', context)
	try:
		select_family =  Family.objects.get(Q(user_id=request.user)|Q(protector=request.user))
	except:
		select_family = None

	context = {
		'apartments':apartments,
		'select_family':select_family,
		'fu_rents': fu_rents,
		'last_rents': last_rents,

	}
	return render(request, 'admin-panel/user/manager/profile.html', context)


@login_required()
def Admin_Profile(request):
	last_charge = Rent.objects.filter(Q(method='NotPaid') ,Q(add_rent_id__pay_time__lte=datetime.now().date()))
	select_user = request.user



	try:
		last_rents = Rent.objects.filter(Q(family_id__protector=request.user) | Q(family_id__user_id=request.user),
										 Q(method='NotPaid'))
	except:
		last_rents = None

	try:
		fu_rents = Rent.objects.filter(Q(family_id__protector=request.user) | Q(family_id__user_id=request.user),
									   Q(method='Online') | Q(method='Cash'))
	except:
		fu_rents = None
	if request.method == 'POST' and 'password' in request.POST:
		old_pass = request.POST['old_password']
		password = request.POST['password']
		re_password = request.POST['re_password']
		test_pass = authenticate(username=select_user.username, password=old_pass)
		# if test_pass:
		# 	return HttpResponse(test_pass)
		# else:
		# 	return HttpResponse('fs')

		if test_pass:
			if password == re_password:
				select_user.set_password(password)
				select_user.save()
				apartments = Apartment.objects.all()
				context = {
					'apartments':apartments,
					'last_charge':last_charge,
					'success': True,
					'pass_change': True,
					'message': 'تغییر رمز با موفقیت انجام شد.',
					'fu_rents': fu_rents,
					'last_rents': last_rents,

				}
				return render(request, 'admin-panel/user/admin/profile.html', context)
			else:
				apartments = Apartment.objects.all()
				context = {
					'last_charge': last_charge,

					'apartments':apartments,
					'error': True,
					'pass_change': True,
					'message': 'لطفا رمز جدید را با دقت وارد کنید.',
					'fu_rents': fu_rents,
					'last_rents': last_rents,

				}
				return render(request, 'admin-panel/user/admin/profile.html', context)
		else:
			apartments = Apartment.objects.all()

			context = {
				'apartments': apartments,
				'last_charge': last_charge,

				'error': True,
				'pass_change': True,
				'message': 'لطفا در صحیح وارد کردن رمز عبور اولیه دقت فرمایید.',
				'fu_rents': fu_rents,
				'last_rents': last_rents,

			}
			return render(request, 'admin-panel/user/admin/profile.html', context)
	if request.method == 'POST' and 'first_name' in request.POST:
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		phone_number = request.POST['phone_number']
		email = request.POST['email']
		select_user.phone_number = phone_number
		select_user.email = email
		select_user.first_name = first_name
		select_user.last_name = last_name
		select_user.save()
		apartments = Apartment.objects.all()

		context = {
			'apartments': apartments,
			'last_charge': last_charge,

			'success': True,
			'infor': True,
			'message': 'مشخصات شما با موفقیت ثبت شد.',
			'fu_rents': fu_rents,
			'last_rents': last_rents,

		}
		return render(request, 'admin-panel/user/admin/profile.html', context)
	try:
		select_family =  Family.objects.get(Q(user_id=request.user)|Q(protector=request.user))
	except:
		select_family = None
	apartments = Apartment.objects.all()

	context = {
		'apartments': apartments,
		'last_charge': last_charge,

		'select_family':select_family,
		'fu_rents': fu_rents,
		'last_rents': last_rents,

	}
	return render(request, 'admin-panel/user/admin/profile.html', context)
