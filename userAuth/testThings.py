from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from datetime import datetime, timedelta, time
from .utils.decorators.login_required import login_required

@csrf_exempt
def lolo(request):
    authorization = request.META['HTTP_AUTHORIZATION']
    session = Session.objects.get(pk=authorization)
    time = session.expire_date
    now = datetime.now()
        
    data = session.get_decoded()
    user = User.objects.get(id=data['_auth_user_id'])
    print(user.username)
    return JsonResponse({'1':1})