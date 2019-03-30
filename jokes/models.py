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
    totalPuntuation = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Jokes'

class Puntuation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joke = models.ForeignKey(Joke,on_delete=models.CASCADE)
    puntuation = models.IntegerField(validators=[validatePunutations])


    class Meta:
        db_table = 'Puntuations'


class FavouriteJoke(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joke = models.ForeignKey(Joke,on_delete=models.CASCADE)

    class Meta:
        db_table = 'FavouriteJokes'