# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User



class RingbackTone(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length='100', null=True, blank=True)
	url = models.URLField()
	count = models.IntegerField(default=0)
	ring_file = models.FileField(upload_to='documents/%Y/%m/%d')
	# created = models.DateTimeField(auto_now_add=True, auto_now=False, default=timezone.now)


class FileTest(models.Model):
	title = models.CharField(max_length='100')
	file_test = models.FileField(upload_to='documents/%Y/%m/%d')


class ImageTest(models.Model):
	file_test = models.FileField()