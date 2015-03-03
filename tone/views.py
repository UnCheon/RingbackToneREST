from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from account.models import UserProfile, Friend
from .models import RingbackTone
from tone.models import *
import json

from gcm import GCM
API_KEY = 'AIzaSyD1JQFF-mkZNzG7-BLJp1v5YMFV9BmTfR0'

def file_upload(request):
	user = User.objects.get(id=1)
	ringbackTone = RingbackTone.objects.create(user=user, title=request.POST['title'], ring_file=request.FILES['file'], url='www.allo.phone')
	return HttpResponse(ringbackTone.ring_file.url)

def image_upload(request):
	image = ImageTest.objects.create(file_test=request.FILES['file'])
	return HttpResponse(image.file_test.url)



def render_json(result):
    result_json = json.dumps(result)
    return HttpResponse(result_json)



def get_my_ringback_tone_list(request):
	if request.method == "GET":
		if request.user.is_authenticated():
			user = request.user
			my_ringback_tone_list = []
			ringback_tones = RingbackTone.objects.filter(user=user)
			for ringback_tone in ringback_tones:
				my_ringback_tone_list.append({'title':ringback_tone.title, 'ring_tone_id':ringback_tone.id, 'ring_tone_url':ringback_tone.ring_file.url})
			return render_json({'status':'success', 'response':my_ringback_tone_list})
		else:
			return HttpResponse('no login')
	else:
		return HttpResponse('not post method')

@csrf_exempt
def change_ringback_tone_friend(request):
	if request.method == "POST":
		if request.user.is_authenticated():
			user = request.user
			ring_tone_id = request.POST['ring_tone_id']
			friend_id = request.POST['friend_id']
			Friend.objects.filter(id=friend_id).update(ring_to_me=ring_tone_id)
			return render_json({'status':'success', 'response':''})
		else:
			return HttpResponse('not login')
	else:
		return HttpResponse('not post method')



	user = User.objects.get(username='01044961101')
	user_friend = User.objects.get(username=request.POST['friend_phone_number'])
	friend = Friend.objects.get(user=user, friend=user_friend)	
	ringback_tone = RingbackTone.objects.get(id=request.POST['ringback_tone_id'])
	friend.ringback_tone = ringback_tone
	friend.save()
	return render_json({'status':'success'})

@csrf_exempt
def upload_ringback_tone(request):
	if request.method == "POST":
		if request.user.is_authenticated():
			user = request.user
			title = request.POST['title']
			ring_file = request.POST['ring_tone_file']
			RingbackTone.objects.create(user=user, ring_file=ring_file, url='www.ring.tone')
			return render_json({'status':'success', 'response':''})
		else:
			return HttpResponse('not login')
	else:
		return HttpResponse('not post method')



@csrf_exempt
def upload_ringback_tone_main(request):
	if request.method == "POST":
		if request.user.is_authenticated():
			user = request.user
			title = request.POST['title']
			ring_file = request.FILES['ringback_tone']

			user_profile = UserProfile.objects.get(user=user)

			old_ringback_tone = user_profile.ring_to_me
			new_ringback_tone = RingbackTone.objects.create(user=user, title=title, url='www.allo.ring', ring_file=ring_file)


			friends = Friend.objects.filter(user=user, ring_to_me=old_ringback_tone).update(ring_to_me=new_ringback_tone)
			# push friends

			return render_json({'status':'success', 'response':''})
		else:
			return HttpResponse('not login')
	else:
		return HttpResponse('not post method')






@csrf_exempt
def upload_ringback_tone_friend(request):
	if request.method == "POST":
		if request.user.is_authenticated():
			user = request.user
			title = request.POST['title']
			ring_file = request.FILES['ringback_tone']
			friend_id = request.POST['friend_id']
			
			ringback_tone = RingbackTone.objects.create(user=user, title=title, url='www.allo.phone', ring_file=ring_file)
			
			friend = Friend.objects.get(id=friend_id)
			friend.ring_to_me = ringback_tone
			
			friend.save()
			update_friends = []
			update_friends.append({'nickname':friend.friend.user_profile.nickname, 'phone_number':friend.friend.user_profile.phone_number, 'friend_id':friend.id, 'ring_to_me_url':friend.ring_to_me.ring_file.url, 'ring_to_me_title':friend.ring_to_me.title, 'ring_to_friend_url':friend.ring_to_friend.ring_file.url, 'ring_to_friend_title':friend.ring_to_friend.title, 'is_new':False})


			
			friend_friend = Friend.objects.get(user=friend.friend, friend=user)
			friend_friend.ring_to_friend = ringback_tone
			friend_friend.is_update = True
			
			friend.friend.user_profile.is_update = True
			
			friend.friend.user_profile.save()
			friend_friend.save()
			# push friend

			gcm = GCM(API_KEY)
			data = {'nickname':friend.user.user_profile.nickname, 'title':friend.ring_to_me.title}
			reg_id = friend.friend.user_profile.device_uuid
			gcm.plaintext_request(registration_id=reg_id, data=data)


			return render_json({'status':'success', 'response':update_friends})
		else:
			return HttpResponse('not login')
	else:
		return HttpResponse('not post')



