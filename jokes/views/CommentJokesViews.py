from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from jokes.models.JokeModel import Joke
from jokes.comments.models import CommentJoke

decorators = [csrf_exempt, login_required]

@method_decorator(csrf_exempt, name='dispatch')
class CommentJokeView(ListView):
    def get(self, request, id):
        comments = CommentJoke.objects.filter(joke=id)
        data = [{'text':i.text,'user':i.user.username} for i in comments]
        return JsonResponse({'data':data},status=200)

    @method_decorator(login_required, name='dispatch')
    def post(self , request):
        try:
            jokeId = request.POST['jokeId']
            text = request.POST['text']
        except Exception:
            raise Exception('Invalid data')
        
        joke = Joke.objects.filter(id=jokeId)

        if len(joke) == 0:
            raise Exception('No joke given')
        
        comment = CommentJoke(user = request.user, joke = joke[0], text = text)
        comment.save()

        return JsonResponse({'data':'Commented succesfully'}, status= 200)

    @method_decorator(login_required, name='dispatch')  
    def delete(self,request,id):
        comment = CommentJoke.objects.filter(id=id)
        if len(comment) == 0:
            raise Exception('No comment given')
        print(request.user.id)
        if comment[0].user.id != request.user.id:
            raise Exception('You can\'t delete other comments')
        
        comment[0].delete()

        return JsonResponse({'data':'Comment removed succesfully'}, status=200)
    

        