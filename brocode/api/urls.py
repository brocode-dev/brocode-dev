from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    # User
    path('registeration/', UserRegistrationView.as_view(), name='registeraton'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('verification/', UserVerificationView.as_view(), name='verification'),
    path('send-mail/', SendMailView.as_view(), name='send-mail'),
    path('get-user/', GetUserView.as_view(), name='get-user'),
    path('update-user/', UpdateUserView.as_view(), name='update-user'),
]
