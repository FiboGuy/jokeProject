from django.contrib.auth.models import User
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.sessions.backends.db import SessionStore
from django.core.files import File
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from .utils.decorators.login_required import login_required
from django.utils.decorators import method_decorator
from .utils.utils import validPassword, validUsername, validEmail, deleteUserImages, login, getUserFromSession
from django.contrib.sessions.models import Session
import time
from datetime import datetime, timedelta

decorators=[csrf_exempt, login_required]

@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(ListView):
    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
            password2 = request.POST['password2']
            email = request.POST['email']
        except Exception:
            return HttpResponse('Invalid credentials', status=400)
            
        try:
            user = User.objects.get(username=username)
        except Exception:
            user = None
    
        if(user is not None):
            return JsonResponse({'data':'username already taken'}, status=400)

        try:
            user = User.objects.get(email=email)
        except Exception:
            user = None
        
        if(user is not None):
            return JsonResponse({'data':'email already registered'}, status=400)
    
        if(validUsername(username) and validPassword(password) and password==password2 and validEmail(email)):
            user = User.objects.create_user(username=username, password=password, email=email)
        else:
            return JsonResponse({'data':'invalid credentials'}, status=400)

        session = login(user)

        return JsonResponse(
            {'data':
                {
                    'data':'register succesfully',
                    'session':session.session_key
                }
            }, status=200)

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(ListView):
    def post(self,request):
        try:
            username=request.POST['username']
            password=request.POST['password']
        except Exception as err:
            return HttpResponse('{} is missing'.format(err), status=400)
        try:
            user = User.objects.get(username=username)
        except Exception:
            try:
                user = User.objects.get(email=username)
            except Exception:
                return JsonResponse({'data':'user not found'}, status=400)
       
        if(check_password(password,user.password)):
            session = login(user)
        else:
            return JsonResponse({'data':'password not valid'}, status=400)

        return JsonResponse(
            {'data':
                {
                    'data':'login succesful',
                    'session':session.session_key,
                    'user': {
                        'id':user.id,
                        'username':user.username,
                        'email':user.email,
                        'first_name':user.first_name,
                        'last_name':user.last_name,
                        'image':user.profile.image.url
                    }
                }
            }, status=200)

@method_decorator(csrf_exempt, name="dispatch")
class LoggedInView(ListView):
    @login_required
    def post(self,request):
        user = getUserFromSession(request.META['HTTP_AUTHORIZATION'], True)
        return JsonResponse({
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'image':user.profile.image.url
        })


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(ListView):
    @login_required
    def post(self, request):
        authorization = request.META['HTTP_AUTHORIZATION']
        Session.objects.get(pk=authorization).delete()
        return JsonResponse({'data':'logged out succesfully'},status=200)


@method_decorator(csrf_exempt, name="dispatch")
class EditProfileView(ListView):
    @login_required
    def post(self, request):
        try:
            username = request.POST['username']
            email = request.POST['email']
            first_name= request.POST['first_name']
            last_name= request.POST['last_name']
        except Exception:
            return HttpResponse('Invalid credentials', status=400)

        try:
            user = User.objects.get(username=username)
        except Exception:
            user = None

        request_user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])

        if(user is not None and user.username != request_user.username):
            return HttpResponse("username already taken", status=400)
        
        try:
            user = User.objects.get(email=email)
        except Exception:
            user = None

        if(user is not None and user.email != request_user.email):
            return HttpResponse("email already in database", status=400)

        if(validUsername(username) and validEmail(email)):
            user = request_user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        else:
            return JsonResponse({'data':'invalid credentials'}, status=400)
        print(request_user.username)
        return JsonResponse({"data":"updated succesfully"})

@method_decorator(csrf_exempt, name="dispatch")
class EditPassword(ListView):
    @login_required
    def post(self, request):
        try:
            password = request.POST['password']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
        except Exception:
            return HttpResponse('missing credentials', status=400)

        user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])

        if not check_password(password,user.password): return HttpResponse('Incorrect password', status=400)
        
        if validPassword(password1) and password1==password2:
            user.password = make_password(password1)
            user.save()
        else:
            return HttpResponse('Not valid password', status=400)
        
        return JsonResponse({'data':'ok'},status=200)
    
@method_decorator(csrf_exempt, name="dispatch")
class UploadImage(ListView):
    @login_required
    def post(self, request):
        try:
            image = request.FILES['image']
        except:
            return HttpResponse('No image', status=400)
        
        request_user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])
  
        deleteUserImages(request_user.username)

        profile = Profile.objects.get(user=request_user)

        profile.image = image
        profile.save()

        return JsonResponse({'data':'ok'},status=200)
        
    @login_required
    def delete(self, request):
        request_user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])
        profile = Profile.objects.get(user=request_user)
        profile.image = 'default/profile.png'
        profile.save()

        deleteUserImages(request_user.username)

        return JsonResponse({'data':'ok'},status=200)