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

class ProfileView(LoginRequiredMixin, CurrentUserIdMixin, TemplateView):
	template_name = 'accounts/profile.html'

	def get(self, request, *args, **kwargs):
		u = get_object_or_404(User, pk=self.current_user_id(request))
		try:
			zone = Zone.objects.get(user_id__exact=u)
			print zone
		except Zone.DoesNotExist:
			return self.render_to_response({})

		return self.render_to_response({'zone':zone})

class AddFriendView(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, CurrentUserIdMixin, View):

	@method_decorator(csrf_protect)
	def dispatch(self, *args, **kwargs):
		return super(AddFriendView, self).dispatch(*args, **kwargs)

	def are_friends(self,u,friend):
		flag=True
		try:
			friend1 = Friend.objects.get(user1__exact=u)
			try:
				friend2 = Friend.objects.get(user2__exact=friend)
			except Friend.DoesNotExist:
				flag=False
		except Friend.DoesNotExist:
			flag = False
		return flag

	def post_ajax(self, request, username):
		u = get_object_or_404(User, pk=self.current_user_id(request))	
		friendname = json.loads(request.POST.get('friendname', None))

		try:
			friend = User.objects.get(username__exact=friendname)
			if (self.are_friends(u,friend)):
				message =json.dumps({'Status':'Already Friends'})
			elif (self.are_friends(friend,u)):
				message =json.dumps({'Status':'Already Friends'})
			else :
				new_friend = Friend(user1=u, user2=friend)
				new_friend.save()

		except User.DoesNotExist:
			message =json.dumps({'Status':'404'})

		message =json.dumps({'Status':'200'})
		return self.render_json_response(message)

class SaveZoneView(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, CurrentUserIdMixin, View):
	
	@method_decorator(csrf_protect)
	def dispatch(self, *args, **kwargs):
		return super(SaveZoneView, self).dispatch(*args, **kwargs)

	def post_ajax(self, request, username):
		u = get_object_or_404(User, pk=self.current_user_id(request))
		zones = json.loads(request.POST.get('zones', None))

		#for now only works for one zone per user
		#for i in range(len(zones)):
		try:
			oldzone=Zone.objects.get(user_id__exact=u)
			oldzone.delete()
			zone = Zone(user = u, lat = zones[0]['lat'],lng = zones[0]['lng'] , radious = (zones[0]['radius']/1000.0))
			zone.save()
		except Zone.DoesNotExist:
			zone = Zone(user = u, lat = zones[0]['lat'],lng = zones[0]['lng'] , radious = (zones[0]['radius']/1000.0))
			zone.save()
		
		message =json.dumps({'Status':'Success'})
		return self.render_json_response(message)

class Circle:
		def __init__(self, lng, lat, radius):
			self.lng, self.lat, self.radius = lng, lat, radius

class CheckZonesView(JSONResponseMixin, AjaxResponseMixin,CurrentUserIdMixin, View):
	
	# A point can be defined by setting the radius at 0.
	count = -1

	
	def comparison(self, P, circle, friends):
		R = 6371 # Earth mean radius
		
		self.count = self.count + 1
		print "amigos: " , friends[self.count]
		

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
			print {'lat':str(circle.lat),'lng' : str(circle.lng),'friend' : str(friends[self.count])}
			return {'lat':str(circle.lat),'lng' : str(circle.lng),'friend' : str(friends[self.count])}
		return None

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(CheckZonesView, self).dispatch(*args, **kwargs)

	def post(self, request, username):
		lat = request.POST.get('lat', None)
		lng = request.POST.get('lng', None)
		P = Circle(float(lat),float(lng),0)
		u = get_object_or_404(User, pk=self.current_user_id(request))
		
		print u.username
		friends1 = Friend.objects.filter(user1_id=u)
		friends2 = Friend.objects.filter(user2_id=u)

		compare = []
		friends = []

		for friendname in friends1:
			print "frinds1: " , friendname
			myfriend = User.objects.get(username__exact=friendname)
			circles = Zone.objects.filter(user=myfriend)
			for zone in circles:
				if str(friendname) != str(u.username):
					print "print teste1: " ,  friendname
					print "print teste2: " ,  u.username

					friends.append(friendname)
					compare.append(zone)
		for friendname in friends2:
			print "frinds2: " , friendname
			myfriend = User.objects.get(username__exact=friendname)
			circles = Zone.objects.filter(user=myfriend)
			for zone in circles:
				if str(friendname) != str(u.username):
					print "print teste1: " ,  friendname
					print "print teste2: " ,  u.username
					friends.append(friendname)
					compare.append(zone)
		# for x in Zone.objects.all():
		# 	print x.lat
		# 	print x.lng
		#P = Circle(float(lat),float(lng),0)
		#print P.lat
		#print [self.comparison(P, i) for i in circles]
		
		message =json.dumps([self.comparison(P, i, friends) for i in compare])
		#print message
		return self.render_json_response(message)