from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from . import utils
from jokes.models.JokeModel import Joke

def validatePunutations(value):
    if value>10 or value<0 :
        raise ValidationError(('%(value)s not in the limit'),
            params={'value': value},
        )

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joke = models.ForeignKey(Joke,on_delete=models.CASCADE)
    rate = models.FloatField(validators=[validatePunutations])

    def __str__(self):
        return "{} rated joke id {} with this puntuation: {}".format(self.user.username, self.joke.id, self.rate)

    class Meta:
        db_table = 'ratings'

@receiver(post_save, sender = Rating)
def save_rate(sender, instance, created, **kwargs):
    rate = utils.calculateTotalRate(instance.joke.id)
    instance.joke.rate = rate
    instance.joke.save()
