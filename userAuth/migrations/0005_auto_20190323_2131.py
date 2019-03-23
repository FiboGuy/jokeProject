# Generated by Django 2.1.7 on 2019-03-23 21:31

from django.db import migrations, models
import userAuth.models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0004_auto_20190323_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='media/default/profile.png', upload_to=userAuth.models.user_directory_path, validators=[userAuth.models.validate_image]),
        ),
    ]
