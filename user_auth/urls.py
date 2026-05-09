from django.urls import path
from .views import *

urlpatterns = [
    path('login_/',login_,name='login_'),
    path('register/',register,name='register'),
    path('profile/',profile,name='profile'),
    path('logout_/',logout_,name='logout_'),
    path('forget_pass/',forget_pass,name='forget_pass'),
    path('reset_pass/',reset_pass,name='reset_pass'),
    path('new_password/',new_password,name='new_password')
]