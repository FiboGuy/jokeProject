from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from userAuth.utils.decorators.login_required import login_required
from userAuth.utils.utils import getUserFromSession
from django.contrib.auth.models import User
from jokes.models.JokeModel import Joke



@method_decorator(csrf_exempt, name='dispatch')
class JokeCreateView(ListView):
    @login_required
    def post(self,request):
        user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])
        try:
            text = request.POST['text']
        except Exception:
            return HttpResponse('No jokes submitted', status=400)
            
        joke = Joke(user=user, text=text)
        joke.save()
        return JsonResponse({'data':{
            'id': joke.id,
            'user':user.username,
            'text':text,
            'created_at':joke.created_at
        }},status=200)
    
@method_decorator(csrf_exempt, name='dispatch')
class JokeView(ListView):
    def get(self,request,id):
        try:
            joke = Joke.objects.get(id=id)
        except Exception:
            return HttpResponse('Joke not found', status=400)
        return JsonResponse({'data':{
            'text':joke.text,
            'rate':joke.rate
        }},status=200)
        
    @login_required
    def delete(self,request,id):
        try:
            joke = Joke.objects.get(id=id)
        except Exception:
            return HttpResponse('Joke not found', status=400)
        
        request_user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])

        if(joke.user.id == request_user.id):
            joke.delete()
            return HttpResponse('Joke with id: {} deleted succesfully'.format(joke.id), status=200)
        else:
            return HttpResponse('Not your joke', status=401)


class JokesUserView(ListView):
    def get(self,request,id):
        try:
            user = User.objects.get(id=id)
        except Exception:
            return HttpResponse('No user found', status=400)
        jokes = Joke.objects.filter(user=id)
        return JsonResponse({user.username:[
            {
                'id':i.id,
                'text':i.text,
                'rate':i.rate,
                'created':i.created_at
                } for i in jokes
        ]}, status = 200)