from django.db import models
from django.contrib.auth.models import User
from .JokeModel import Joke

class FavouriteJoke(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joke = models.ForeignKey(Joke, on_delete=models.CASCADE)

    def __str__(self):
        return "{} likes joke with id {}".format(self.user.username,self.joke.id)

    class Meta:
        db_table = 'favouriteJokes'