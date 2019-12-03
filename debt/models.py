from django.db import models
from structure.models import *

from django.db.models.signals import post_save ,pre_save , post_delete ,m2m_changed
from django.dispatch import receiver

from datetime import datetime
# Create your models here.
class Add_Rent(models.Model):
	SUBJECT = (
		('Water','water'),
		('Charge','charge'),
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	subject = models.CharField(max_length=128,choices=SUBJECT)
	title = models.CharField(max_length=64,null=True,blank=True)
	description = models.TextField()
	price = models.CharField(max_length=6)
	pay_time = models.DateField()
	apartment_id = models.ForeignKey(Apartment,on_delete=models.CASCADE)

	def __str__(self):
		return self.apartment_id.name +' '+ self.title


@receiver(post_save,sender=Add_Rent)
def AddAllRent(sender,instance,created, **kwargs):
	if created:
		unites = instance.apartment_id.unit.select_related().all()

		for unit in unites:
			if unit.rent_status != 'empty':
				rent = Rent.objects.create(add_rent_id=instance,family_id=unit.family_id)

		rents = Rent.objects.filter(add_rent_id=instance)
		for rent in rents:
			if instance.subject == 'Water':
				rent.price = int(rent.family_id.number) * int(instance.price)
			else:
				rent.price = instance.price
			rent.save()


# else:
	# 	unites = instance.apartment_id.unit.select_related().all()
	# 	for unit in unites:
	# 		try:
	# 			rent = Rent.objects.get(add_rent_id=instance,family_id=unit.family_id)
	# 			rent.
	# 		except:
	# 			pass

@receiver(pre_delete,sender = Add_Rent)
def DeleteAllRent(sender,instance,*args,**kwargs):
	rents = Rent.objects.filter(add_rent_id=instance)
	for rent in rents:
		rent.delete()



class Rent(models.Model):
	PAYMENT_METHOD = (
		('NotPaid','not paid'),
		('Online','online'),
		('Cash','cash')
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	add_rent_id = models.ForeignKey(Add_Rent,on_delete=models.CASCADE)
	family_id = models.ForeignKey(Family,on_delete=models.CASCADE)
	method = models.CharField(max_length=32,choices=PAYMENT_METHOD,default='NotPaid')
	payment_date = models.DateField(blank=True,null=True)
	price = models.CharField(max_length=6)

	def save(self, *args , **kwargs):
		if self.method == 'Cash' or self.method == 'Online':
			self.payment_date = datetime.now().date()
		#
		# if self.add_rent_id.subject == 'Water':
		# 	self.price = int(self.add_rent_id.price) * int(self.family_id.number)
		# else:
		# 	self.price = self.add_rent_id.price

		super(Rent, self).save(*args, **kwargs)

	def __str__(self):
		return self.add_rent_id.title + ' ' + self.family_id.protector.get_full_name()+ 'آیدی' +str(self.pk)


# @receiver(post_save,sender=Rent)
# def AddPaymentDate(sender,instance,created, **kwargs):
# 	if instance.method == 'Cash' or instance.method == 'Online':
# 		server_date = datetime.now().date()
# 		instance.payment_date = se


class Add_Damage(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=64, null=True, blank=True)
	description = models.TextField()
	price = models.CharField(max_length=6)
	pay_time = models.DateTimeField()
	unit_id = models.ManyToManyField(Unit)

	def __str__(self):
		return self.title + ' ' +str(self.unit_id.count())


@receiver(m2m_changed,sender=Add_Damage.unit_id.through)
def AddAllDaage(sender, instance, action, reverse, pk_set, **kwargs):
	if action == 'post_add':
		unites = pk_set


		for unit in unites:
			unit = Unit.objects.get(pk=unit)
			if unit.rent_status != 'empty':
				damage = Damage.objects.create(add_damage_id=instance,family_id=unit.family_id)

	elif action == 'post_remove':
		unites = pk_set

		for unit in unites:
			unit = Unit.objects.get(pk=unit)

			damage = Damage.objects.get(add_damage_id=instance,family_id=unit.family_id)
			damage.delete()
				# damage = Damage.objects.create(add_mage_id=instance,family_id=unit.family_id)

class Damage(models.Model):
	PAYMENT_METHOD = (
		('NotPaid', 'not paid'),
		('Online', 'online'),
		('Cash', 'cash')
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	add_damage_id = models.ForeignKey(Add_Damage, on_delete=models.CASCADE)
	family_id = models.ForeignKey(Family, on_delete=models.CASCADE)
	method = models.CharField(max_length=32, choices=PAYMENT_METHOD, default='NotPaid')

	def __str__(self):
		return self.add_damage_id.title + ' ' + self.family_id.protector.get_full_name()

