import json, urllib, hashlib, datetime

from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.sessions.models import Session
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect , csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404 , get_list_or_404 , render_to_response
from meet_me_at_the_corner import settings
from django.conf import settings
from braces.views import LoginRequiredMixin



class CurrentUserIdMixin(object):
	def current_user_id(self,request):
		session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
		session = Session.objects.get(session_key=session_key)
		uid = session.get_decoded().get('_auth_user_id')
		return uid