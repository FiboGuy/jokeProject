from django.urls import path
from . import views

urlpatterns=[
    path('follow', views.followView.as_view() , name="follow"),
    path('follow/<int:id>', views.followView.as_view(), name="followers")
]