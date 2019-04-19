from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from userAuth.utils.decorators.login_required import login_required
from userAuth.utils.utils import getUserFromSession
from django.contrib.auth.models import User
from .models import Followers


@method_decorator(csrf_exempt, name='dispatch')
class followView(ListView):
    def get(self,request, id):
        users = Followers.objects.filter(followed=id)
        data = [i.follower.username for i in users]
        return JsonResponse({'data':data})

    @login_required
    def post(self,request):
        user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])
        try:
            followedUsername = request.POST['user']
        except Exception:
            return HttpResponse('No user provided', status=400)
        
        try:
            followedUser = User.objects.get(username = followedUsername)
        except Exception:
            return HttpResponse('Trying to follow a not existing user', status = 400)

        if user==followedUser: 
            return HttpResponse('You can\'t follow yourself', status = 400)

        check = Followers.objects.filter(follower=user.id, followed=followedUser.id)

        if len(check)==0:
            follow = Followers(follower=user, followed=followedUser)
            follow.save()
            return JsonResponse({'data':'Followed succesfully'}, status=200)
        else:
            return JsonResponse({'data':'Already following'}, status=400)
    
    @login_required
    def delete(self,request,id):
        user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])
        check = Followers.objects.filter(follower=user.id, followed=id)

        if len(check)==0:
            data = {'data':'You are not following this user'}
        else:
            check[0].delete()
            data = {'data':'You stopped following this user'}
        
        return JsonResponse(data,status=200)
        