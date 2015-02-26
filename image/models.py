# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User


class RingbackImage(models.Model):
	user = models.ForeignKey(User)
	url = models.URLField()
	count = models.IntegerField(default=0)
