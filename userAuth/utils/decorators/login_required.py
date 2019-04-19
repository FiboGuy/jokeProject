from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.contrib.auth.models import User
from datetime import datetime

def login_required(function):
    def wrapper(self, request):
       
        try:
            authorization = request.META['HTTP_AUTHORIZATION']
            session = Session.objects.get(pk=authorization)
        except Exception:
            return HttpResponse('Unauthorized 1', status=401)
        if(session.expire_date<datetime.now()):
            session.delete()
            return HttpResponse('Unauthorized 2', status=401)
        return function(self, request)
    return wrapper
