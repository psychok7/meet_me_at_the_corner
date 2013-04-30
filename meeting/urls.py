from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from meeting.views import SaveZoneView , CheckZonesView , AddFriendView



urlpatterns = patterns('',
						url(r'^meeting/add_friend$', AddFriendView.as_view(), name='add_friend'),
                        url(r'^meeting/save_zone$', SaveZoneView.as_view(), name='save_zone'),
                        url(r'^meeting/check_zone$', CheckZonesView.as_view(), name='check_zone'),

)