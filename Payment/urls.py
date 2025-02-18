from django.contrib import admin
from django.urls import path
from .views.login import Login, logout
from .views.signup import Signup
from .views.profile import Userprofile, update_profile
from Payment.middlewares.auth import auth_middleware

urlpatterns = [
    path('signup', Signup.as_view()),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('userprofile', auth_middleware(Userprofile.as_view()), name='userprofile'),
    path('update_profile/<int:id>', update_profile, name='update_profile'),
]