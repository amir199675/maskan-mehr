from django.db import models
from django.contrib.auth.models import AbstractUser

import os

from django.db.models.signals import post_save ,pre_delete
from django.dispatch import receiver
# Create your models here.


class MyUser(AbstractUser):
	national_number = models.CharField(max_length=11,unique=True,null=True,blank=True)
	phone_number = models.CharField(max_length=11,null=True,blank=True)
	birth_day = models.DateField(null=True,blank=True)
	picture = models.ImageField(upload_to='users-pic/',blank=True,null=True)

	def __str__(self):
		return self.username + ' ' + self.get_full_name()
	#
	# def save(self, *args, **kwargs):
	# 	self.set_password(self.password)
	# 	super(MyUser, self).save(*args, **kwargs)

class Family (models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	user_id = models.ManyToManyField(MyUser,related_name='user_id',null=True,blank=True)
	protector = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='protector_id')
	number = models.IntegerField()
	def __str__(self):
		return self.protector.get_full_name() + ' ' + str(self.number) + ' ' + self.protector.username

	def family_name(self):
		return  'خانواده ' + self.protector.last_name

def delete_image(path):
	if os.path.isfile(path):
		os.remove(path)

@receiver(pre_delete , sender = MyUser)
def delete_pictures(sender,instance,*args,**kwargs):
	if instance.picture:
		delete_image(instance.picture.path)
