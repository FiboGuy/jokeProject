from django.urls import path
from .views.FavouriteJokeViews import FavouriteJokeView
from .views.JokeViews import JokeCreateView, JokeView, JokesUserView
from .views.FavouriteJokeViews import FavouriteJokeView
from .views.RatingViews import RateJokeView
from .views.CommentJokesViews import CommentJokeView

urlpatterns = [
    path('new', JokeCreateView.as_view(), name='new_joke'),
    path('joke/<int:id>', JokeView.as_view(), name='joke'),
    path('jokes/<int:id>', JokesUserView.as_view(), name='jokes_user'),
    path('rate', RateJokeView.as_view(), name='joke_rate'),
    path('favourite', FavouriteJokeView.as_view(),name='joke_favourite'),
    path('favourite/<int:id>', FavouriteJokeView.as_view(),name='joke_favourite_id'),
    path('comment', CommentJokeView.as_view(), name='comment_joke' ),
    path('comment/<int:id>', CommentJokeView.as_view(),name='get_comment')
]