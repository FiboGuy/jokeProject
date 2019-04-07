from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse, resolve
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.urls import reverse
from emailService.emails.resetPassword import urlResetPassword
import time

@require_http_methods(['POST'])
@csrf_exempt
def generateResetUrl(request):
    email = request.POST['email']
    user = User.objects.filter(email=email)
    if len(user)==0:
        raise Exception('Email not found')

    s = SessionStore()
    s['email'] = email
    s['time'] = time.time()
    s.set_expiry(60*5)
    s.save()

    url = request.build_absolute_uri(reverse(resetUrl, args=(s.session_key,)))
    urlResetPassword(email,{'url':url})

    return HttpResponse("ok")

def resetUrl(request, key):
    try:
        session = Session.objects.get(pk=key)
    except Exception:
        raise Http404('Session expired')
    data = session.get_decoded()
    expired_time = data['time']+data['_session_expiry']
    time_now = time.time()
    if expired_time < time_now:
        session.delete()
        raise Http404('Session expired')

    return HttpResponse('Url created correctly')

# password change
