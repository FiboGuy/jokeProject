from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validatePunutations(value):
    if value>10 or value<0 :
        raise ValidationError(('%(value)s not in the limit'),
            params={'value': value},
        )

class Joke(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    totalPuntuation = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'Jokes'

class Puntuation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joke = models.ForeignKey(Joke,on_delete=models.CASCADE)
    puntuation = models.IntegerField(validators=[validatePunutations])

    def __str__(self):
        return "{} rated joke id {} with this puntuation: {}".format(self.user.username, self.joke, self.puntuation)

    class Meta:
        db_table = 'Puntuations'


class FavouriteJoke(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joke = models.ForeignKey(Joke,on_delete=models.CASCADE)

    def __str__(self):
        return "{} likes joke with id {}".format(self.user.username,self.joke)

    class Meta:
        db_table = 'FavouriteJokes'