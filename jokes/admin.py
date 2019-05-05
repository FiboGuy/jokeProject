from django.contrib import admin
from .comments.models import CommentJoke
from .models import FavouriteJokeModel
from .models import JokeModel
# Register your models here.

admin.site.register(CommentJoke)
admin.site.register(FavouriteJokeModel.FavouriteJoke)
admin.site.register(JokeModel.Joke)

