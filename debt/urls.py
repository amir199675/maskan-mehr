from django.urls import path
from debt.views import *
from django.conf import settings
from django.conf.urls.static import static
from .manager import *

app_name = 'Debt'
urlpatterns = [
    path('', Index.as_view(),name='index'),
    path('apartments/', ApartmentListView.as_view(),name='apartment-list'),
    path('charges/', RentListView.as_view(),name='rent-list'),
    path('waters/', WaterBillView.as_view(),name='water-list'),
    path('payment/<id>/', Rent_Details,name='rent-details'),
    path('<id>/add_charge/', Manager_Add_Rent,name='add-charge-manager'),
    path('<id>/add_water/', Manager_Add_Watert,name='add-water-manager'),

    path('Manager/not-paid/<id>/', Not_Paid_People,name='not-paid'),
    path('Manager/payment/<id>/', Manager_Payment, name='manager-payment'),


    path('Manager/families/<id>/', All_Families, name='all-family'),



    path('coming-soon/' , Coming_Soon,name='coming-soon')
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
