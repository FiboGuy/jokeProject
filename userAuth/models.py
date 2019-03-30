from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
# Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.username, filename)

def validate_image(value):
    filesize = value.size
    if filesize > 1048576:
        raise ValidationError("The maximum file size that can be uploaded is 1MB")
    else:
        return value


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to=user_directory_path, validators=[validate_image], default='default/profile.png')
    updated_at = models.DateTimeField(auto_now=True)
    # active boolean field for email activation account.

    def __str__(self):
        return self.user.username

    class Meta:
        db_table='profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    


