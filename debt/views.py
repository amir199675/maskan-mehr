from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin ,UserPassesTestMixin
from django.contrib.auth.models import Permission

from django.db.models import Q

from django.shortcuts import get_object_or_404 , get_list_or_404

from django.utils.decorators import method_decorator

from django.shortcuts import render ,HttpResponse ,Http404 ,redirect

from django.contrib.auth.models import Group

from datetime import datetime

from django.views.generic import TemplateView ,View , ListView , DetailView

from main.models import  *
from structure.models import *
from debt.models import *

# Create your views here.

def Sidbar(user):
	select_user = user
	groups = Group.objects.all()
	try:
		user_groups = select_user.groups.all()
		for group in groups:
			for user_group in user_groups:
				if group.name == user_group.name and user_group.name == 'Manager':
					return 'Manager'
				elif group.name == user_group.name and user_group.name == 'Admin':
					return 'Admin'
	except:
		pass

class Index (View):
	template_name = 'main-site/index.html'

	def get(self, request, *args, **kwargs):
		sliders = Slider.objects.filter(status='Public')

		context = {
			'index':True,
		    'sliders':sliders
				   }

		return render(request, self.template_name, context)

# @method_decorator(login_required)

class ApartmentListView(LoginRequiredMixin,UserPassesTestMixin,ListView):

	model = Apartment
	context_object_name = 'apartments'
	template_name = 'admin-panel/apartment/list.html'

	def test_func(self):
		return self.request.user.is_staf


class RentListView(LoginRequiredMixin,ListView):
	template_name = 'admin-panel/rent/list.html'

	def get(self, request, *args, **kwargs):
		# login_user = self.request.user
		family = get_object_or_404(Family,Q(protector=self.request.user)|Q(user_id=self.request.user))
		rents = Rent.objects.filter(family_id=family,add_rent_id__subject='Charge')
		# return HttpResponse(rents.count())
		server_date= datetime.today().date()
		context = {
			'warning':True,
			'message':'برای مرتب سازی بر روی هر کدام از ستون های مورد نظر کلیک کنید',
			'rents':rents,
			'server_date':server_date,
		}
		return render(request,self.template_name,context)

@login_required()
def Rent_Details(request,id):

	family = Family.objects.get(Q(protector=request.user)|Q(user_id=request.user))
	select_rent = get_object_or_404(Rent,pk=id,family_id = family)
	server_date = datetime.today().date()
	context = {
		'server_date':server_date,
		'select_rent':select_rent
	}
	return render(request,'admin-panel/rent/details.html',context)



class WaterBillView(LoginRequiredMixin,ListView):
	template_name = 'admin-panel/water/list.html'

	def get(self, request, *args, **kwargs):
		# login_user = self.request.user

		family = get_object_or_404(Family,Q(protector=self.request.user)|Q(user_id=self.request.user))
		rents = Rent.objects.filter(family_id=family,add_rent_id__subject='Water')
		# return HttpResponse(rents.count())
		server_date= datetime.today().date()
		context = {
			'rents':rents,
			'server_date':server_date,
		}
		return render(request,self.template_name,context)



@login_required()
def Water_Details(request,id):

	# family = Family.objects.get(Q(protector=request.user)|Q(user_id=request.user))
	select_rent = get_object_or_404(Rent,pk=id)

	server_date = datetime.today().date()

	context = {
		'server_date':server_date,
		'select_rent':select_rent
	}
	return render(request,'admin-panel/water/details.html',context)


@login_required()
def Coming_Soon(request):
	message = 'این قابلیت در آینده اضافه خواهد شد'
	context = {
		'message':message
	}
	return render(request,'admin-panel/coming-soon/coming-soon.html',context)