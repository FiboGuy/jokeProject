from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Followers(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followedUser')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followerUser')

    def __str__(self):
        return "{} following {}".format(self.follower,self.followed)

    class Meta:
        db_table = 'followers'

