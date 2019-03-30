from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Followers


# decorators=[login_required, csrf_exempt]
@method_decorator(csrf_exempt, name='dispatch')
class followView(ListView):
    @method_decorator(login_required,name='dispatch')
    def post(self,request):
        user = request.user
        try:
            followedUsername = request.POST['user']
        except Exception:
            raise Exception('Not user provided')
        
        try:
            followedUser = User.objects.get(username=followedUsername)
        except Exception:
            raise Exception('Trying to follow a not existing user')

        if user==followedUser: 
            raise Exception('You can\'t follow yourself')

        check = Followers.objects.filter(follower=user.id, followed=followedUser.id)

        if len(check)==0:
            follow = Followers(follower=user, followed=followedUser)
            follow.save()
            return JsonResponse({'data':'ok'}, status=200)
        else:
            return JsonResponse({'data':'Already following'}, status=400)
        
    def get(self,request, id):
        users = Followers.objects.filter(followed=id)
        data = [i.follower.username for i in users]
        return JsonResponse({'data':data})