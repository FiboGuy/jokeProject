from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from userAuth.utils.decorators.login_required import login_required
from userAuth.utils.utils import getUserFromSession
from jokes.models.JokeModel import Joke
from .utils import validateRating
from .models import Rating


@method_decorator(csrf_exempt, name='dispatch')
class RateJokeView(ListView):
    @login_required
    def post(self,request):
        user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])
        try:
            rate = float(request.POST['rate'])
            jokeId = request.POST['jokeId']
        except Exception:
            return HttpResponse('Invalid post information', status=400)

        try:
            joke = Joke.objects.get(id=jokeId)
        except Exception:
            return HttpResponse('No joke found', status=400)
        
        if not validateRating(int(rate)):
            return HttpResponse('Invalid rate', status=400)

        if joke.user == user:
            return HttpResponse('You can\'t rate your jokes', status=400)

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