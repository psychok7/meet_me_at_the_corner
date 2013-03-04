from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template , redirect_to
from meet_me_at_the_corner import settings
from meeting.views import LoggedInView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$',direct_to_template, {'template': 'index.html'}, name='index'),
                    url(r'^index',direct_to_template, {'template': 'index.html'}, name='index'),
                    url(r'^logged-in/$', LoggedInView.as_view(), name='logged-in'),
                    url(r'', include('social_auth.urls')),
                    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                    url(r'^admin/', include(admin.site.urls)),
                    url(r'^(?P<username>[-\w]+)/$',direct_to_template,{'template': 'accounts/profile.html'}, name='profile'),
                    (r'^users/(?P<username>[-\w]+)/$', redirect_to, {'url': '/%(username)s/'}),
                    (r'^accounts/', include('registration.backends.simple.urls')),
                    (r'^(?P<username>[-\w]+)/', include('meeting.urls')),
                    (r'^media/(?P<path>.*)$', 'django.views.static.serve',  
                    {'document_root': settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'keepitsafesite.views.home', name='home'),
    # url(r'^keepitsafesite/', include('keepitsafesite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # # Uncomment the next line to enable the admin:
    #  url(r'^admin/', include(admin.site.urls)),
)
