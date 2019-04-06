# Generated by Django 2.1.7 on 2019-04-06 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jokes.models.RatingModel


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteJoke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'favouriteJokes',
            },
        ),
        migrations.CreateModel(
            name='Joke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=420)),
                ('rate', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jokes',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(validators=[jokes.models.RatingModel.validatePunutations])),
                ('joke', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jokes.Joke')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ratings',
            },
        ),
        migrations.AddField(
            model_name='favouritejoke',
            name='joke',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jokes.Joke'),
        ),
        migrations.AddField(
            model_name='favouritejoke',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
