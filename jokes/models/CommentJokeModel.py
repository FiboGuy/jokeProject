from django.db import models
from django.contrib.auth.models import User
from jokes.models.JokeModel import Joke

class CommentJoke(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    joke = models.ForeignKey(Joke, related_name='joke', on_delete=models.CASCADE)
    text = models.TextField(blank=False, max_length=280)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return 'Comment from {}'.format(self.user.username)

    class Meta:
        db_table = 'comments'

