# Generated by Django 2.1.7 on 2019-04-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0010_remove_profile_resetpassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='session',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
