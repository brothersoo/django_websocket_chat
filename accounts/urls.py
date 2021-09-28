from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import UserLoginView, UserRegistrationView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
