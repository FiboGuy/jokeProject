from django.contrib.auth.models import User
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .utils import validPassword, validUsername, validEmail
import json


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(ListView):
    def post(self, request):
        data = json.loads(request.body)
        try:
            username = data['username']
            password = data['password']
            password = data['password2']
            email = data['email']
        except Exception as err:
            raise Exception("{} is missing".format(err))

        try:
            user = User.objects.get(username=username)
        except Exception:
            user = None
    
        if(user is not None):
            return JsonResponse({'data':'username already taken'}, status=400)

        try:
            user = User.objects.get(email=data["email"])
        except Exception:
            user = None
        
        if(user is not None):
            return JsonResponse({'data':'email already registered'}, status=400)
    
        if(validUsername(data['username']) and validPassword(data['password']) and data['password']==data['password2'] and validEmail(data['email'])):
            user = User.objects.create_user(username=username, password=password, email=email)
        else:
            return JsonResponse({'data':'invalid credentials'}, status=400)

        login(request,user)

        return JsonResponse({"data":"Registered succesfully"},status=200)

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(ListView):
    def post(self,request):
        data = json.loads(request.body)
        try:
            username=data['username']
            password=data['password']
        except Exception as err:
            raise Exception('{} is missing'.format(err))
        
        try:
            user = User.objects.get(username=username)
        except Exception:
            try:
                user = User.objects.get(email=username)
            except Exception:
                return JsonResponse({'data':'user not found'}, status=401)
        
        if(check_password(password,user.password)):
            login(request,user)
        else:
            return JsonResponse({'data':'password not valid'}, status=401)

        return JsonResponse({'data':'login succesful'}, status=200)

@method_decorator(login_required, name="dispatch")
class LoggedInView(ListView):
    def get(self,request):
        user = request.user
        return JsonResponse({
            'username':user.username,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name
        })

@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(ListView):
    def post(self, request):
        logout(request)
        return JsonResponse({'data':'logged out succesfully'},status=200)

decorators=[csrf_exempt, login_required]
@method_decorator(decorators, name="dispatch")
class EditProfileView(ListView):
    def put(self, request):
        #edit user profile
        return JsonResponse({"ok":"ok"})
