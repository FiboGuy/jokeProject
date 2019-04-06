from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from jokes.models.JokeModel import Joke
from jokes.models.FavouriteJokeModel import FavouriteJoke

decorators=[csrf_exempt,login_required]

@method_decorator(decorators, name='dispatch')
class FavouriteJokeView(ListView):
    def get(self,request):
        user = request.user
        jokes = FavouriteJoke.objects.filter(user=user)

        return JsonResponse({
            'jokes':[
                {
                    'user':joke.user.username,
                    'text':joke.joke.text,
                    'rate':joke.joke.rate,
                    'created_at':joke.joke.created_at
                } for joke in jokes
            ]
        },status=200)

    def post(self,request):
        user = request.user
        try:
            joke = request.POST['joke']
        except Exception:
            raise Exception('No joke submitted')

        try:
            joke = Joke.objects.get(id=joke)
        except Exception:
            raise Exception('Joke doesn\'t exists')

        favourite = FavouriteJoke.objects.filter(user=user,joke=joke)

        if len(favourite)==0:
            favourite = FavouriteJoke(user=user,joke=joke)
            favourite.save()
            data = {'data':'Saved succesfully'}
        else:
            data = {'data':'You already liked it'}
        
        return JsonResponse(data,status=200)
    
    def delete(self,request, id):
        user = request.user

        favourite = FavouriteJoke.objects.filter(user=user,joke=id)
        if len(favourite)==0:
            data = {'data':'It\'s not on your favourites list'}
        else:
            favourite[0].delete()
            data = {'data':'Deleted from favourites succesfully'}
        
        return JsonResponse(data,status=200)