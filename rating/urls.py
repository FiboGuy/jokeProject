from django.urls import path
from .views import RateJokeView

urlpatterns = [
    path('rate', RateJokeView.as_view(), name='joke_rate')
]