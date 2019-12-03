from django.db import models
from structure.models import *
# Create your models here.
class Question(models.Model):
	STATUS = (
		('Open','open'),
		('Close','close'),
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=64)
	content = models.TextField()
	status = models.CharField(max_length=32,choices=STATUS)
	apartment_id = models.ForeignKey(Apartment,on_delete=models.CASCADE)

	def __str__(self):
		return self.title + ' ' + self.apartment_id.name

class Comment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=32,null=True,blank=True)
	content = models.TextField()
	user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE)
	question_id = models.ForeignKey(Question,on_delete=models.CASCADE)

	def __str__(self):
		return self.user_id.get_full_name() + ' ' + self.question_id.title

class Result (models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=64)
	content = models.TextField()
	question_id = models.ForeignKey(Question,on_delete=models.CASCADE)

	def __str__(self):
		return self.title+ ' ' + self.question_id.title
