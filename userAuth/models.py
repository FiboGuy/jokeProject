from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.


def user_directory_path(instance, filename):
    print(instance.user)
    return 'user_{0}/{1}'.format(instance.user.username, filename)

def validate_image(value):
    filesize= value.size
    if filesize > 1048576:
        raise ValidationError("The maximum file size that can be uploaded is 1MB")
    else:
        return value


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to=user_directory_path, validators=[validate_image])

    def __str__(self):
        return self.user.username


