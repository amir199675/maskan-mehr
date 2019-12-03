from django.db import models

# Create your models here.
class Slider(models.Model):
	STATUS = (
		('Public','public'),
		('Draft','draft'),
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=64)
	description = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='slider-pic/')
	status = models.CharField(max_length=32,choices=STATUS)


	def __str__(self):
		return self.title

