# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

import json
import md5
 
from .models import UserProfile, Friend, Contact
from image.models import RingbackImage
from tone.models import RingbackTone
   
import logging


def render_json(result):
    result_json = json.dumps(result)
    return HttpResponse(result_json)



@csrf_exempt
def register(request):
	if request.method == "POST":
		phone_number = request.POST['phone_number']
		nickname = request.POST['nickname']
		device_uuid = request.POST['device_uuid']
		device_type = request.POST['device_type']
		password = md5.md5(request.POST['device_type']).hexdigest()
		ring_to_me = RingbackTone.objects.get(id=1)

		try: 
			user = User.objects.create(username=phone_number, password=password)
			try:
				user_profile = UserProfile.objects.create(user=user, nickname=nickname, phone_number=phone_number, device_uuid=device_uuid, device_type=device_type, ring_to_me=ring_to_me)
				login_user = authenticate(username=phone_number, password=request.POST['device_type'])
				login(request, login_user)
				try:
					contacts = Contact.objects.filter(phone_number=phone_number).select_related()
					for contact in contacts:
						friend_friend = Friend.objects.create(user=contact.user, friend=user, ring_to_me=contact.user.user_profile.ring_to_me, ring_to_friend=user.user_profile.ring_to_me)
						# push to friend
						contact.friend = friend_friend
						contact.is_friend = True
						contact.save()
						friend_user_profile = contact.user.user_profile
						friend_user_profile.is_update = True
						friend_user_profile.save()
				except:	
					pass
				return render_json({'status':'success'})
			except:
				try:
					user.delete()
					return HttpResponse('user.delete success')
				except:
					return HttpResponse('user.delete error')
		except:
			try:
				user = User.objects.get(username=phone_number)
				try:
					user_profile = UserProfile.objects.get(user=user)
					login_user = authenticate(username=phone_number, password=request.POST['device_type'])
					login(request, login_user)
					return render_json({'status':'success'})
				except:
					try:
						user_profile = UserProfile.objects.create(user=user, nickname=nickname, phone_number=phone_number, device_uuid=device_uuid, device_type=device_type, ring_to_me=ring_to_me)
						login_user = authenticate(username=phone_number, password=request.POST['device_type'])
						login(request, login_user)
						return render_json({'status':'success'})
					except:
						user.delete()
						return render_json({'user is alread exist. user.delete success'})
			except:
				return render_json({'status':'fail 3'})
	else:
		return render_json({'status':'fail 4', 'response':'not post access'})



@csrf_exempt
def rb_login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		# the password verified for the user
		if user.is_active:
			login(request, user)
			return HttpResponse("User is valid, active and authenticated")
		else:
			return HttpResponse("The password is valid, but the account has been disabled!")
	else:
		# the authentication system was unable to verify the username and password
		return HttpResponse("The username and password were incorrect.")







@csrf_exempt
def sycn_friends(request):
	LOG_FILENAME = 'login.log'
	logging.basicConfig(filename='/home/DjangoProjects/sync.log',level=logging.DEBUG)    
	logging.info("Running Urban Planning")
	

	if request.method == "POST":
		if request.user.is_authenticated():
		# if 1 == 1:			
			contacts = request.POST['contacts']
			contacts_json = json.loads(contacts)
			new_friends = []
			
			user = request.user
			# user = User.objects.get(username='01044961101')

			friend = Friend
			friend_friend = Friend
			contact = Contact 

			ring_to_me_title = ''
			ring_to_me_url = ''
			image_to_me_title = ''
			image_to_me_url = ''

			count = 0


			for contact_json in contacts_json:
				try:
					contact = Contact.objects.get(user=user, phone_number=contact_json['phone_number'])
				except:
					contact = Contact.objects.create(user=user, phone_number=contact_json['phone_number'])

				try:
					# check my contact is user or not user
					user_friend = User.objects.get(username=contact_json['phone_number'])
					# make friend
					friend = Friend.objects.create(user=user, friend=user_friend, ring_to_me=user.user_profile.ring_to_me, ring_to_friend=user_friend.user_profile.ring_to_me)
					contact.is_friend = True
					contact.friend = friend
					contact.save()
					# new_friends.append({'nickname':user_friend.user_profile.nickname, 'phone_number':contact.phone_number, 'friend_id':friend.id, 'ring_to_me_url':friend.ring_to_me.url, 'ring_to_me_title':friend.ring_to_me.title, 'ring_to_friend_url':friend.ring_to_friend.url, 'ring_to_friend_title':friend.ring_to_friend.title, 'is_new':True})
					new_friends.append({'nickname':user_friend.user_profile.nickname, 'phone_number':contact.phone_number, 'friend_id':friend.id, 'ring_to_me_url':friend.ring_to_me.ring_file.url, 'ring_to_me_title':friend.ring_to_me.title, 'ring_to_friend_url':friend.ring_to_friend.ring_file.url, 'ring_to_friend_title':friend.ring_to_friend.title, 'is_new':True})
				except:
					pass
			return render_json({'status':'success', 'response':new_friends})
		else:
			return HttpResponse('not login')
	else:
		return HttpResponse('not post')




def update_check(request):
	if request.method == "GET":
		if request.user.is_authenticated():
			user = request.user
			user_profile = UserProfile.objects.get(user=user)

			new_friends = []
			if user_profile.is_update == True:
				# when got new friend
				friends_new = Friend.objects.filter(user=user, is_new=True)
				for friend in friends_new:
					new_friends.append({'nickname':friend.friend.user_profile.nickname, 'phone_number':friend.friend.user_profile.phone_number, 'friend_id':friend.id, 'ring_to_me_url':friend.ring_to_me.ring_file.url, 'ring_to_me_title':friend.ring_to_me.title, 'ring_to_friend_url':friend.ring_to_friend.ring_file.url, 'ring_to_friend_title':friend.ring_to_friend.title, 'is_new':True})
				friends_new.update(is_new=False)
				# when changed ring_to_friend
				friends_update = Friend.objects.filter(user=user, is_update=True)
				for friend in friends_update:
					new_friends.append({'nickname':friend.friend.user_profile.nickname, 'phone_number':friend.friend.user_profile.phone_number, 'friend_id':friend.id, 'ring_to_me_url':friend.ring_to_me.ring_file.url, 'ring_to_me_title':friend.ring_to_me.title, 'ring_to_friend_url':friend.ring_to_friend.ring_file.url, 'ring_to_friend_title':friend.ring_to_friend.title, 'is_new':False})
				friends_update.update(is_update=False)
				user_profile.is_update = False
				user_profile.save()
			return render_json({'status':'success', 'response':new_friends})
		else:
			return HttpResponse('not login')
	else:
		return HttpResponse('get page')


def get_all_friends(request):
	if request.method == "GET":
		if request.user.is_authenticated():
			user = request.user
			my_friends = []
			friends = Friend.objects.filter(user=user)
			for friend in friends:
				my_friends.append({'nickname':friend.friend.user_profile.nickname, 'phone_number':friend.friend.user_profile.phone_number, 'friend_id':friend.id, 'ring_to_me_url':friend.ring_to_me.ring_file.url, 'ring_to_me_title':friend.ring_to_me.title, 'ring_to_friend_url':friend.ring_to_friend.ring_file.url, 'ring_to_friend_title':friend.ring_to_friend.title})
			return render_json({'status':'success', 'response':my_friends})
		else:
			return HttpResponse('not login')
	else:
		return HttpResponse('not get access')




'''
def friends(request):
	if request.method == "GET":
		if request.user.is_authenticated():
			user = request.user
			friends = Friend.objects.filter(user=user)
			for friend in friends:
				ringback_tone = ''
				if friend.ringback_tone is None:
					ringback_tone = friend.friend.user_profile.ringback_tone
				else:
					ringback_tone = friend.ringback_tone
'''

				






