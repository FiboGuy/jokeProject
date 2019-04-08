from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse, resolve
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .utils import validPassword
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

@require_http_methods(['GET'])
def resetUrl(request, key):
    try:
        session = Session.objects.get(pk=key)
    except Exception:
        raise Http404()
    data = session.get_decoded()

    if timeExpired(data):
        session.delete()
        raise Http404('Session expired')
        
    return JsonResponse({'data':{
        'email':data['email'],
        'key':session.session_key
    }}, status = 200)

@require_http_methods(['POST'])
@csrf_exempt
def resetPassword(request):
    key = request.POST['key']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    
    try:
        session = Session.objects.get(pk=key)
    except Exception:
        raise Http404()

    data = session.get_decoded()
    if timeExpired(data):
        session.delete()
        raise Http404('Session expired')
    
    try:
        user = User.objects.get(email=data['email'])
    except Exception:
        raise Exception('No user found with that email')
    
    if validPassword(password1) and password1==password2:
        user.password = make_password(password1)
        user.save()
    else:
        raise Exception('Invalid credentials')
    
    session.delete()
    
    return HttpResponse('Password changed correctly')
    
def timeExpired(data):
    expired_time = data['time'] + data['_session_expiry']
    time_now = time.time()
    if expired_time <= time_now:
        return True
    return False





