from django.urls import path
from . import views

urlpatterns = [
    path('new', views.NewJokeView.as_view(), name="Joke")
]