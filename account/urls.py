from django.urls import path
from debt.views import *
from django.contrib.auth.views import LoginView , LogoutView
from .views import *
from .other_views import *

app_name = 'Account'
urlpatterns = [
	path('Accounts/Login/', Login, name='login'),
	path('Profile/',Profile, name='profile'),
	path('Manager/Profile/',Manager_Profile, name='manager_profile'),
	path('Admin/Profile/',Admin_Profile, name='admin_profile'),
	path('Logout/',LogoutView.as_view(template_name='admin-panel/user/logout.html'),name='logout')
]
