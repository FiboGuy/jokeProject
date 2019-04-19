from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from userAuth.utils.decorators.login_required import login_required
from userAuth.utils.utils import getUserFromSession
from jokes.models.JokeModel import Joke
from jokes.models.FavouriteJokeModel import FavouriteJoke



@method_decorator(csrf_exempt, name='dispatch')
class FavouriteJokeView(ListView):
    @login_required
    def get(self,request):
        user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])
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

    @login_required
    def post(self,request):
        user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])
        try:
            joke = request.POST['joke']
        except Exception:
            return HttpResponse('No joke submitted', status=400)

        try:
            joke = Joke.objects.get(id=joke)
        except Exception:
            return HttpResponse('Joke doesn\'t exists', status=400)

        favourite = FavouriteJoke.objects.filter(user=user,joke=joke)

        if len(favourite)==0:
            favourite = FavouriteJoke(user=user,joke=joke)
            favourite.save()
            data = {'data':'Saved succesfully'}
        else:
            data = {'data':'You already liked it'}
        
        return JsonResponse(data,status=200)
        
    @login_required
    def delete(self,request, id):
        user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])

        favourite = FavouriteJoke.objects.filter(user=user,joke=id)
        if len(favourite)==0:
            data = {'data':'It\'s not on your favourites list'}
        else:
            favourite[0].delete()
            data = {'data':'Deleted from favourites succesfully'}
        
        return JsonResponse(data,status=200)