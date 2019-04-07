from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from jokes.models.JokeModel import Joke
from jokes.utils import validateRating
from jokes.models.RatingModel import Rating

decorators=[csrf_exempt,login_required]

@method_decorator(decorators, name='dispatch')
class RateJokeView(ListView):
    def post(self,request):
        user = request.user
        try:
            rate = float(request.POST['rate'])
            jokeId = request.POST['jokeId']
        except Exception:
            raise Exception('Invalid post information')

        try:
            joke = Joke.objects.get(id=jokeId)
        except Exception:
            raise Exception('No joke found')
        
        if not validateRating(int(rate)):
            raise Exception('Invalid rate')

        if joke.user == user:
            raise Exception('You can\'t rate your jokes')

        rating = Rating.objects.filter(user=user,joke=joke)

        if len(rating)==0:
            rating = Rating(user=user,joke=joke,rate=rate)
        else:
            rating=rating[0]
            rating.rate = rate
            
        rating.save()

        return JsonResponse({'data':{
            'joke':rating.joke.id,
            'user':rating.user.username,
            'rate':rating.rate,
            'jokeRate':rating.joke.rate
        }})