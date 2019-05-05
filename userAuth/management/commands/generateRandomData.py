from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from userAuth.models import Profile
from jokes import models
from rating.models import Rating
from followers.models import Followers
from jokes.comments.models import CommentJoke
from faker import Faker
import random
import requests

faker=Faker()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = generateRandomUsers(self)
        generateFollows(self, users)
        jokes = generateJokes(self, users)
        generateFavourites(self,users,jokes)
        generateRatings(self, users, jokes)
        generateComments(self, users, jokes)

        self.stdout.write(self.style.SUCCESS('Successfully generated data'))

def generateRandomUsers(BaseCommand):
    users=[]
    for i in range(20):
        username = faker.user_name()
        email = faker.email()
        password = 'lolo'
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile(user = user).save()
            BaseCommand.stdout.write(BaseCommand.style.HTTP_INFO('Created user with username {}'.format(user.username)))
            users.append(user)
        except:
            continue
    return users

def generateFollows(BaseCommand, users):
    for i in range(40):
        followed = random.choice(users)
        follower = random.choice(users)

        while followed == follower:
            follower = random.choice(users)
        
        follow = Followers.objects.get_or_create(follower=follower, followed=followed)
        BaseCommand.stdout.write(BaseCommand.style.HTTP_INFO('follow: {}'.format(follow[0])))

def generateJokes(BaseCommand, users):
    jokes = []
    for i in range(80):
        user = random.choice(users)
        joke_text = requests.get('https://api.chucknorris.io/jokes/random').json()['value']
        joke = models.JokeModel.Joke(user=user, text=joke_text)
        joke.save()
        jokes.append(joke)
        BaseCommand.stdout.write(BaseCommand.style.HTTP_INFO('user {} created joke: {}'.format(user,joke)))
    return jokes


def generateFavourites(BaseCommand, users, jokes):
    for i in range(30):
        joke = random.choice(jokes)
        user = random.choice(users)
        while joke.user == user:
            user = random.choice(users)
        models.FavouriteJokeModel.FavouriteJoke.objects.get_or_create(user = user, joke = joke)
        BaseCommand.stdout.write(BaseCommand.style.HTTP_INFO('user {} created favourite joke id: {}'.format(user,joke.id)))
       

def generateRatings(BaseCommand, users, jokes):
    for i in range(160):
        joke = random.choice(jokes)
        user = random.choice(users)
        while joke.user == user:
            user = random.choice(users)
        
        rate = round(random.random()*10,2)

        rating = Rating.objects.filter(user = user, joke = joke)

        if len(rating)==0:
            rating = Rating(user = user, joke = joke, rate = rate)
        else:
            rating = rating[0]
            rating.rate = rate

        rating.save()
        BaseCommand.stdout.write(BaseCommand.style.HTTP_INFO('user {} rated joke {} with rate: {}'.format(user,joke.id,rate)))

def generateComments(BaseCommand, users, jokes):
    for i in range(40):
        joke = random.choice(jokes)
        user = random.choice(users)
        text = faker.text()
        CommentJoke(joke = joke, user = user, text = text).save()
        BaseCommand.stdout.write(BaseCommand.style.HTTP_INFO('user {} commented joke id: {}'.format(user,joke.id)))


        
        