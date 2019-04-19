from django.urls import path
from .views import RegisterView, LoginView , LoggedInView, LogoutView, EditProfileView, EditPassword, UploadImage
from .resetPassword import generateResetUrl, resetUrl, resetPassword
from .testThings import lolo

urlpatterns=[
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('loggedin', LoggedInView.as_view(),name='loggedIn'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('edit', EditProfileView.as_view(), name='editProfile'),
    path('editPassword', EditPassword.as_view(), name='editPassword'),
    path('uploadImage', UploadImage.as_view(), name='uploadImage'),
    path('generateResetUrl', generateResetUrl, name='generate_reset_url'),
    path('resetUrl/<str:key>', resetUrl, name='reset_url'),
    path('resetPassword', resetPassword, name='reset_password'),
    path('lolo', lolo, name='test_lolo')
]