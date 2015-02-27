from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from account.models import UserProfile, Friend
from .models import RingbackTone
from tone.models import *
import json

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



@csrf_exempt
def upload_ringback_tone_main(request):
	# if request.user.is_authenticated():
    # Do something for authenticated users.
	# else:
    # Do something for anonymous users.
		# pass:

	# user = requset.user
	user = User.objects.get(username='01044961101')

	# s3 upload code... and later
	url = 'aws.s3.upload'
	ringback_tone = RingbackTone.objects.create(user=user, url=url)
	user.user_profile.ringback_tone = ringback_tone
	user.user_profile.save()

	return render_json({'status':'success'})

	

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
			friend.is_update = True
			
			friend.save()
			update_friends = []
			update_friends.append({'nickname':friend.friend.user_profile.nickname, 'phone_number':friend.friend.user_profile.phone_number, 'friend_id':friend.id, 'ring_to_me_url':friend.ring_to_me.ring_file.url, 'ring_to_me_title':friend.ring_to_me.title, 'ring_to_friend_url':friend.ring_to_friend.ring_file.url, 'ring_to_friend_title':friend.ring_to_friend.title, 'is_new':False})


			try:
				friend_friend = Friend.objects.get(user=friend.user, friend=user)
				friend_friend.ring_to_me = ringback_tone
				friend_friend.is_update = True
				
				friend.user.user_profile.is_update = True
				
				friend.user.user_profile.save()
				friend_friend.save()
			except:
				pass
			
			# push friend
			return render_json({'status':'success', 'response':update_friends})
		else:
			return HttpResponse('not login')
	else:
		return HttpResponse('not post')



@csrf_exempt
def change_ringback_tone_friend(request):
	user = User.objects.get(username='01044961101')
	user_friend = User.objects.get(username=request.POST['friend_phone_number'])
	friend = Friend.objects.get(user=user, friend=user_friend)	
	ringback_tone = RingbackTone.objects.get(id=request.POST['ringback_tone_id'])
	friend.ringback_tone = ringback_tone
	friend.save()
	return render_json({'status':'success'})