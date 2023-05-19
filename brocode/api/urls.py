from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    # User
    path('registeration/', UserRegistrationView.as_view(), name='registeraton'),
    path('verification/', UserVerification.as_view(), name='verification')
]