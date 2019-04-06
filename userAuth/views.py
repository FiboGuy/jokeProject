from django.contrib.auth.models import User
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login, logout
from django.core.files import File
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .utils import validPassword, validUsername, validEmail, deleteUserImages


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(ListView):
    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
            password2 = request.POST['password2']
            email = request.POST['email']
        except Exception as err:
            raise Exception(err)
    
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

        login(request,user)

        return JsonResponse({"data":"Registered succesfully"},status=200)

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(ListView):
    def post(self,request):
        try:
            username=request.POST['username']
            password=request.POST['password']
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
        if(user.profile.image):
            image=user.profile.image.url
        else:
            image=None
        return JsonResponse({
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'image':image
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
        try:
            username = request.POST['username']
            email = request.POST['email']
            first_name= request.POST['first_name']
            last_name= request.POST['last_name']
        except Exception as err:
            raise Exception(err)

        try:
            user = User.objects.get(username=username)
        except Exception:
            user = None

        if(user is not None and user.username != request.user.username):
            raise Exception("username already taken")
        
        try:
            user = User.objects.get(email=email)
        except Exception:
            user = None

        if(user is not None and user.email != request.user.email):
            raise Exception("email already in database")

        if(validUsername(username) and validEmail(email)):
            user = request.user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        else:
            return JsonResponse({'data':'invalid credentials'}, status=400)

        return JsonResponse({"daga":"updated succesfully"})

#Añadir image upload y password change

decorators=[csrf_exempt, login_required]
@method_decorator(decorators, name="dispatch")
class EditPassword(ListView):
    def post(self, request):
        try:
            password = request.POST['password']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
        except Exception:
            raise Exception('missing credentials')

        user = request.user

        if not check_password(password,user.password): raise Exception('Incorrect password')
        
        if validPassword(password1) and password1==password2:
            user.password = make_password(password1)
            user.save()
            login(request,user)
        else:
            raise Exception('Not valid password')
        
        return JsonResponse({'data':'ok'},status=200)
    
decorators=[csrf_exempt, login_required]
@method_decorator(decorators, name="dispatch")
class UploadImage(ListView):
    def post(self, request):
        try:
            image = request.FILES['image']
        except:
            raise Exception('No image')
        
        deleteUserImages(request.user.username)

        profile = Profile.objects.get(user=request.user)

        profile.image = image
        profile.save()

        return JsonResponse({'data':'ok'},status=200)
    
    def delete(self, request):
        profile = Profile.objects.get(user=request.user)
        profile.image = 'default/profile.png'
        profile.save()

        deleteUserImages(request.user.username)

        return JsonResponse({'data':'ok'},status=200)