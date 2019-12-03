from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin ,UserPassesTestMixin
from django.contrib.auth.models import Permission

from django.db.models import Q

from django.shortcuts import get_object_or_404 , get_list_or_404

from django.utils.decorators import method_decorator

from django.shortcuts import render ,HttpResponse ,Http404

from datetime import datetime

from django.views.generic import TemplateView ,View , ListView , DetailView

from main.models import  *
from structure.models import *
from debt.models import *


