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
from datetime import datetime
from django.contrib.auth.models import Group
from jdatetime import JalaliToGregorian, GregorianToJalali


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
						'apartments': apartments,
						'status': 'Manager',
					}
					return info
				elif group.name == user_group.name and user_group.name == 'Admin':
					return 'Admin'
	except:
		return 'User'


@login_required()
def Manager_Add_Rent(request, id):
	select_apartment = get_object_or_404(Apartment, manager_id=request.user, pk=id)

	logged = Sidbar(request.user)

	if logged['status'] == 'Manager':
		apartments = logged['apartments']
	# return HttpResponse(apartments)
	else:
		apartments = None

	if request.method == 'POST':
		title = request.POST['title']
		pay_time = request.POST['pay_time']
		description = request.POST['description']
		price = request.POST['price']
		try:
			pay_time = datetime.strptime(pay_time, '%Y/%m/%d')
			day = pay_time.day
			year = pay_time.year
			month = pay_time.month
			date = JalaliToGregorian(year, month, day)
			date = date.getGregorianList()
			year = date[0]
			month = date[1]
			day = date[2]
			make_format = str(year) + '-' + str(month) + '-' + str(day)
			pay_time = datetime.strptime(make_format, '%Y-%m-%d')
		except:
			pay_time = None
		try:
			rent = Add_Rent.objects.create(subject='Charge', pay_time=pay_time, description=description, title=title,
										   apartment_id_id=id, price=price)
		except:
			return HttpResponse('nashod')

		message = '{} با موفقیت اضافه شد'.format(rent.title)
		context = {
			'select_apartment':select_apartment,

			'apartments': apartments,
			'success': True,
			'message': message
		}
		return render(request, 'admin-panel/rent/manager/add-charge.html', context)
	context = {
		'select_apartment': select_apartment,

		'apartments': apartments,
	}
	return render(request, 'admin-panel/rent/manager/add-charge.html', context)


@login_required()
def Manager_Add_Watert(request, id):
	select_apartment = get_object_or_404(Apartment, manager_id=request.user, pk=id)

	logged = Sidbar(request.user)

	if logged['status'] == 'Manager':
		apartments = logged['apartments']
	# return HttpResponse(apartments)
	else:
		apartments = None

	if request.method == 'POST':
		title = request.POST['title']
		pay_time = request.POST['pay_time']
		description = request.POST['description']
		price = request.POST['price']
		try:
			pay_time = datetime.strptime(pay_time, '%Y/%m/%d')
			day = pay_time.day
			year = pay_time.year
			month = pay_time.month
			date = JalaliToGregorian(year, month, day)
			date = date.getGregorianList()
			year = date[0]
			month = date[1]
			day = date[2]
			make_format = str(year) + '-' + str(month) + '-' + str(day)
			pay_time = datetime.strptime(make_format, '%Y-%m-%d')
		except:
			pay_time = None
		try:
			rent = Add_Rent.objects.create(subject='Water', pay_time=pay_time, description=description, title=title,
										   apartment_id_id=id, price=price)
		except:
			return HttpResponse('nashod')

		message = '{} با موفقیت اضافه شد'.format(rent.title)
		context = {
			'select_apartment':select_apartment,
			'apartments': apartments,
			'success': True,
			'message': message
		}
		return render(request, 'admin-panel/rent/manager/add-water.html', context)

	context = {
		'select_apartment': select_apartment,

		'apartments': apartments,
	}
	return render(request, 'admin-panel/rent/manager/add-water.html', context)


def Not_Paid_People(request, id):
	select_apartment = get_object_or_404(Apartment, manager_id=request.user, pk=id)
	logged = Sidbar(request.user)
	if logged['status'] == 'Manager':
		apartments = logged['apartments']
	# return HttpResponse(apartments)
	else:
		apartments = None
	peoples = Rent.objects.filter(method='NotPaid' ,add_rent_id__apartment_id=select_apartment)
	server_date=datetime.now().date()
	context = {
		'select_apartment': select_apartment,

		'server_date':server_date,
		'apartments':apartments,
		'warning': True,
		'message': 'برای مرتب سازی بر روی هر کدام از ستون های مورد نظر کلیک کنید',
		'rents':peoples,

	}
	return render(request,'admin-panel/rent/manager/notpaidlist.html',context)

def Manager_Payment(request,id):
	select_rent = Rent.objects.get(id = id)
	select_apartment = get_object_or_404(Apartment,manager_id = request.user ,pk=select_rent.add_rent_id.apartment_id.id)
	server_date = datetime.now().date()
	select_rent = Rent.objects.get(id=id)
	days_left = datetime.now().date() - select_rent.add_rent_id.pay_time
	days_left = days_left.days
	logged = Sidbar(request.user)
	if logged['status'] == 'Manager':
		apartments = logged['apartments']
	# return HttpResponse(apartments)
	else:
		apartments = None
	if request.method == 'POST' and 'pay' in request.POST:
		rent = select_rent
		rent.method = 'Cash'
		rent.save()
		peoples = Rent.objects.filter(method='NotPaid', add_rent_id__apartment_id=select_apartment)
		server_date = datetime.now().date()
		context = {
			'select_apartment':select_apartment,
			'server_date': server_date,
			'apartments': apartments,
			'success':True,
			'message': 'شارژ مورد نظر با موفقیت پرداخت گردید',
			'rents': peoples,

		}

		return render(request,'admin-panel/rent/manager/notpaidlist.html',context)

	context = {
		'apartments':apartments,
		'server_date': server_date,
		'days_left':days_left,
		'select_rent':select_rent
	}
	return render(request,'admin-panel/rent/manager/user-rent-details.html',context)

def All_Families(request,id):
	select_apartment = get_object_or_404(Apartment, manager_id=request.user, pk=id)
	not_paids = {}
	# rents = Rent.objects.filter(add_rent_id__apartment_id=select_apartment,method='NotPaid')
	units = Unit.objects.filter(Q(rent_status='protector')|Q(rent_status='tenant'),apartment_id=select_apartment)
	for unit in units:
		try:
			np = Rent.objects.filter(add_rent_id__apartment_id=select_apartment,method='NotPaid',family_id=unit.family_id).count()
		except:
			np = 0
		not_paids[unit.id] = np

	logged = Sidbar(request.user)
	if logged['status'] == 'Manager':
		apartments = logged['apartments']
	# return HttpResponse(apartments)
	else:
		apartments = None

	context = {
		'select_apartment':select_apartment,
		'apartments':apartments,
		'not_paids':not_paids,
		'units':units
	}
	return render(request,'admin-panel/family/manager/list.html',context)