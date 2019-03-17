from django.urls import path
from .views import RegisterView, LoginView , LoggedInView, LogoutView, EditProfileView

urlpatterns=[
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('loggedin', LoggedInView.as_view(),name='loggedIn'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('edit', EditProfileView.as_view(), name='editProfile')
]