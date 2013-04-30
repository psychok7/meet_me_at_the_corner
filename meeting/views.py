# Create your views here.
import json , urllib2

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect , csrf_exempt
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404 , get_list_or_404, render_to_response
from django.template import RequestContext
from braces.views import LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin
from datetime import datetime, date
from meeting.mixins import CurrentUserIdMixin
from django.utils.decorators import method_decorator
from django.conf import settings
from meeting.models import Friend , Zone
from math import sqrt, pi, sin, cos, atan2
from decimal import *


class LoggedInView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		url = '/%s/' % self.request.user.username
		return HttpResponseRedirect(url)

class AddFriendView(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, CurrentUserIdMixin, View):

	@method_decorator(csrf_protect)
	def dispatch(self, *args, **kwargs):
		return super(AddFriendView, self).dispatch(*args, **kwargs)

	def post_ajax(self, request, username):
		u = get_object_or_404(User, pk=self.current_user_id(request))	
		message =json.dumps({'Status':'Success'})
		return self.render_json_response(message)

class SaveZoneView(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, CurrentUserIdMixin, View):
	
	@method_decorator(csrf_protect)
	def dispatch(self, *args, **kwargs):
		return super(SaveZoneView, self).dispatch(*args, **kwargs)

	def post_ajax(self, request, username):
		u = get_object_or_404(User, pk=self.current_user_id(request))
		zones = json.loads(request.POST.get('zones', None))

		for i in range(len(zones)):
			# circles = Zone.objects.filter(user=u) \
			# 	& Zone.objects.filter(lat__exact=zones[i]['lat']) \
			# 		& Zone.objects.filter(lng__exact=zones[i]['lng'])
			# print "try" , circles
			# if not circles:
			zone = Zone(user = u, lat = zones[i]['lat'],lng = zones[i]['lng'] , radious = (zones[i]['radius']/1000.0))
			zone.save()
		
		message =json.dumps({'Status':'Success'})
		return self.render_json_response(message)

class Circle:
		def __init__(self, lng, lat, radius):
			self.lng, self.lat, self.radius = lng, lat, radius

class CheckZonesView(JSONResponseMixin, CurrentUserIdMixin, View):
	
	# A point can be defined by setting the radius at 0.


	def comparison(self, P, circle):
		R = 6371 # Earth mean radius

		circle.lat = float(circle.lat)
		circle.lng = float(circle.lng)
		dLat = (circle.lat - P.lat)*pi/180.0
		dLon = (circle.lng - P.lng)*pi/180.0
		lat1 = P.lat*pi/180.0
		lat2 = circle.lat*pi/180.0
		# print lat2

		a = sin(dLat/2) * sin(dLat/2) + \
		        sin(dLon/2) * sin(dLon/2) * cos(lat1) * cos(lat2) 
		
		dist = R * (2 * atan2(sqrt(a), sqrt(1-a)))
		
		if dist <= float(circle.radious):
			return 'LAT: ' + str(circle.lat)+' LNG:'+ str(circle.lng) + 'sep'
		return 'sep'

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(CheckZonesView, self).dispatch(*args, **kwargs)

	def post(self, request, username):
		lat = request.POST.get('lat', None)
		lng = request.POST.get('lng', None)
		username = request.POST.get('username', None)
		#print username
		#circles = [Circle(38.730519,-9.14653, 12.5), Circle(3.5, 4.5, 10), Circle(12.0, 10.0, 0.5)]
		u = User.objects.get(username__contains=username)
		circles = Zone.objects.filter(user=u)
		for x in Zone.objects.all():
			print x.lat
			print x.lng
		P = Circle(float(lat),float(lng),0)
		#print P.lat
		#print [self.comparison(P, i) for i in circles]

		message =json.dumps([self.comparison(P, i) for i in circles])
		print message
		return self.render_json_response(message)