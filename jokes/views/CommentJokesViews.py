from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from userAuth.utils.decorators.login_required import login_required
from userAuth.utils.utils import getUserFromSession
from jokes.models.JokeModel import Joke
from jokes.comments.models import CommentJoke


@method_decorator(csrf_exempt, name='dispatch')
class CommentJokeView(ListView):
    def get(self, request, id):
        comments = CommentJoke.objects.filter(joke=id)
        data = [{'text':i.text,'user':i.user.username} for i in comments]
        return JsonResponse({'data':data},status=200)

    @login_required
    def post(self , request):
        try:
            jokeId = request.POST['jokeId']
            text = request.POST['text']
        except Exception:
            return HttpResponse('Invalid data', status=400)
        
        joke = Joke.objects.filter(id=jokeId)

        if len(joke) == 0:
            return HttpResponse('No joke given', status=400)
        
        request_user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])

        comment = CommentJoke(user = request_user, joke = joke[0], text = text)
        comment.save()

        return JsonResponse({'data':'Commented succesfully'}, status= 200)

    @login_required 
    def delete(self,request,id):
        comment = CommentJoke.objects.filter(id=id)
        if len(comment) == 0:
            return HttpResponse('No comment given', status=400)

        request_user = getUserFromSession(request.META['HTTP_AUTHORIZATION'])

        if comment[0].user.id != request_user.id:
            return HttpResponse('You can\'t delete other comments', status=400)
        
        comment[0].delete()

        return JsonResponse({'data':'Comment removed succesfully'}, status=200)
    

        