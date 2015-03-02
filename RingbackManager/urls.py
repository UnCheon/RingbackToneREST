from django.conf.urls import patterns, include, url
from django.contrib import admin
from account.views import *
from tone.views import *
from image.views import *
from django.conf import settings

urlpatterns = patterns('',

	# TEST
	(r'^file_upload/$', file_upload),
	(r'^image_upload/$', image_upload),

	# ACCOUNT
	(r'^account/register/$', register),
	(r'^account/login/$', rb_login),
	(r'^account/update/check/$', update_check),
	(r'^account/sync/friends/$', sycn_friends),


	# Ringback Tone
	(r'^ringback/tones/$', get_my_ringback_tone_list),
	(r'^ringback/tone/upload/main/$', upload_ringback_tone_main),
	(r'^ringback/tone/upload/friend/$', upload_ringback_tone_friend),
	(r'^ringback/tone/change/friend/$', change_ringback_tone_friend),
	# (r'^ringback/tone/play/$', play_ringback_tone),


	# Ringbak Image
	(r'^ringback/image/upload/main/$', upload_ringback_image_main),
	(r'^ringback/image/upload/friend/$', upload_ringback_image_friend),
	(r'^ringback/image/change/friend/$', change_ringback_image_friend),
	# (r'^ringback/image/play/$', play_ringback_image),


    # Examples:
    # url(r'^$', 'RingbackManager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    
)
