from django.urls import path
from . import views

urlpatterns = [
    path('new', views.JokeCreateView.as_view(), name='new_joke'),
    path('joke/<int:id>', views.JokeView.as_view(), name='joke')
]