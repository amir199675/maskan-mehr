from django.db import models
from account.models import *
# Create your models here.
class Apartment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=128)
	address = models.TextField()
	manager_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)

	class Meta:
		permissions = (
			('can_read','can read'),
		)

	def __str__(self):
		return self.name + ' ' +self.manager_id.get_full_name()

class Unit(models.Model):
	RENT_STATUS = (
		('empty','Empty'),
		('protector','Protector'),
		('tenant','Tenant')
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	apartment_id = models.ForeignKey(Apartment,on_delete=models.CASCADE,related_name='unit')
	floor = models.CharField(max_length=32)
	plaque = models.IntegerField()
	family_id = models.ForeignKey(Family,related_name='fu',on_delete=models.CASCADE,null=True,blank=True)
	rent_status = models.CharField(max_length=32,choices=RENT_STATUS,default='empty')
	owner_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return self.apartment_id.name + ' طبقه ' + str(self.floor) + ' پلاک ' + str(self.plaque)

	def address(self):
		return  ' طبقه ' + str(self.floor) + ' پلاک ' + str(self.plaque)


