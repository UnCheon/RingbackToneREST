from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from account.models import UserProfile, Friend
from django.contrib.auth.models import User
from .models import RingbackImage
import json




def render_json(result):
    result_json = json.dumps(result)
    return HttpResponse(result_json)


@csrf_exempt
def upload_ringback_image_main(request):
	# if request.user.is_authenticated():
    # Do something for authenticated users.
	# else:
    # Do something for anonymous users.
		# pass:

	# user = requset.user
	user = User.objects.get(username='01044961101')

	# s3 upload code... and later
	url = 'aws.s3.upload'
	ringback_image = RingbackImage.objects.create(user=user, url=url)
	user.user_profile.ringback_image = ringback_image
	user.user_profile.save()

	return render_json({'status':'success'})

	

@csrf_exempt
def upload_ringback_image_friend(request):
	# if request.user.is_authenticated():
    # Do something for authenticated users.
	# else:
    # Do something for anonymous users.
		# pass:
	# user = requset.user
	user = User.objects.get(username='01044961101')
	user_friend = User.objects.get(username=request.POST['friend_phone_number'])
	friend = Friend.objects.get(user=user, friend=user_friend)
		
	# s3 upload code... and later
	url = 'aws.s3.upload'
	ringback_image = RingbackImage.objects.create(user=user, url=url)
	friend.ringback_image = ringback_image
	friend.save()
	return render_json({'status':'success'})

@csrf_exempt
def change_ringback_image_friend(request):
	user = User.objects.get(username='01044961101')
	user_friend = User.objects.get(username=request.POST['friend_phone_number'])
	friend = Friend.objects.get(user=user, friend=user_friend)	
	ringback_image = RingbackImage.objects.get(id=request.POST['ringback_image_id'])
	friend.ringback_image = ringback_image
	friend.save()
	return render_json({'status':'success'})
