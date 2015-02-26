# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from tone.models import RingbackTone




	
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='user_profile')
	nickname = models.CharField(max_length='80')
	phone_number = models.CharField(max_length='30', unique=True)
	device_uuid = models.CharField(max_length='100', null=False, unique=True)
	device_type = models.CharField(max_length='80', null=False, unique=False)
	ring_to_me = models.ForeignKey(RingbackTone, null=True, blank=True)
	is_update = models.BooleanField(default=False)
	def __unicode__(self):
		return '%s' % (self.nickname)	


class Friend(models.Model):
	user = models.ForeignKey(User, related_name='user')
	friend = models.ForeignKey(User, related_name='friend')
	ring_to_me = models.ForeignKey(RingbackTone, related_name='ring_to_me', default=1)
	ring_to_friend = models.ForeignKey(RingbackTone, related_name='ring_to_friend', default=1)
	message = models.CharField(max_length='80', default='')
	is_new = models.BooleanField(default=True)
	is_update = models.BooleanField(default=False)
	def __unicode__(self):
		return '%s' % (self.user.username+'s friend '+self.friend.username)	
	def get_message(self):
		return self.message
	def get_ring_to_me(self):
		if self.ring_to_me is None:
			return '%s' % (self.user.user_profile.ring_to_me.url)
		else:
			return '%s' % (self.ring_to_me.url)	
	def get_ring_to_friend(self):
		if self.ring_to_friend is None:
			return '%s' % (self.friend.user_profile.ring_to_friend.url)
		else:
			return '%s' % (self.ring_to_friend.url)			





class Contact(models.Model):
	user = models.ForeignKey(User, related_name='contact')
	phone_number = models.CharField(max_length='30')
	friend = models.OneToOneField(Friend, null=True, blank=True, related_name='contact')
	is_friend = models.BooleanField(default=False)
	def __unicode__(self):
		return '%s' % (self.phone_number)	
