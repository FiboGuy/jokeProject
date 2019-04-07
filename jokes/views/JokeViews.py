from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from jokes.models.JokeModel import Joke

decorators=[csrf_exempt,login_required]

@method_decorator(decorators, name='dispatch')
class JokeCreateView(ListView):
    def post(self,request):
        user = request.user
        try:
            text = request.POST['text']
        except Exception:
            raise Exception('No jokes submitted')
            
        joke = Joke(user=user, text=text)
        joke.save()
        return JsonResponse({'data':{
            'id': joke.id,
            'user':user.username,
            'text':text,
            'created_at':joke.created_at
        }},status=200)
    
@method_decorator(decorators, name='dispatch')
class JokeView(ListView):
    def get(self,request,id):
        try:
            joke = Joke.objects.get(id=id)
        except Exception:
            raise Exception('Joke not found')
        return JsonResponse({'data':{
            'text':joke.text,
            'rate':joke.rate
        }},status=200)
        
    def delete(self,request,id):
        try:
            joke = Joke.objects.get(id=id)
        except Exception:
            raise Exception('Joke not found')
        if(joke.user.id == request.user.id):
            joke.delete()
            return HttpResponse('Joke with id: {} deleted succesfully'.format(joke.id))
        else:
            raise Exception('Not your joke')


class JokesUserView(ListView):
    def get(self,request,id):
        try:
            user = User.objects.get(id=id)
        except Exception:
            raise Exception('No user found')
        jokes = Joke.objects.filter(user=id)
        return JsonResponse({user.username:[
            {
                'id':i.id,
                'text':i.text,
                'rate':i.rate,
                'created':i.created_at
                } for i in jokes
        ]})