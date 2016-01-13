from punchclock.models import ClockSession

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

import datetime

# core logic

@login_required
def index(request):	
	try:
		current_cs = ClockSession.objects.get(user = request.user, clocked_in = True)
	except ClockSession.DoesNotExist:
		current_cs = None
	except ClockSession.MultipleObjectsReturned:
		return HttpResponse('An error has occurred. Multiple unclosed clock-ins are recorded. ' + 
							'Please ask an admin to manually clock you out of a previous session.')

	# https://stackoverflow.com/questions/1622038/find-mondays-date-with-python
	today = datetime.date.today()
	last_monday = today - datetime.timedelta(days = today.weekday())
	recent_sessions = ClockSession.objects.filter(user = request.user, in_time__gte = last_monday)
	
	return render(request, 'punchclock/index.html', {'cs': current_cs, 'user': request.user, 'rs': recent_sessions})

@login_required
def clock_in(request):
	try:
		cs = ClockSession.objects.get(user = request.user, clocked_in = True)
		return HttpResponseRedirect(reverse('punchclock:index'))
	except ClockSession.DoesNotExist:
		cs = ClockSession(user = request.user)
		cs.clock_in()
		return HttpResponseRedirect(reverse('punchclock:index'))

@login_required
def clock_out(request):
	try:
		cs = ClockSession.objects.get(user = request.user, clocked_in = True)
		cs.clock_out()
		return HttpResponseRedirect(reverse('punchclock:index'))
	except ClockSession.DoesNotExist:
		return HttpResponseRedirect(reverse('punchclock:index'))
	except ClockSession.MultipleObjectsReturned:
		return HttpResponse('Error: You are clocked in multiple times. Please have an admin correct this manually.')

# login procedures

def employee_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username = username, password = password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('punchclock:index'))
			else:
				return HttpResponse('Unauthorized User')
		else:
			return HttpResponse('Invalid Login Credentials')
	else:
		return render(request, 'punchclock/login.html')

@login_required
def employee_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('punchclock:index'))