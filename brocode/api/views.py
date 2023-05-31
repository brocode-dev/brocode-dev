"""
User Views.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils.renderers import UserJSONRenderer
from rest_framework.generics import RetrieveUpdateAPIView

from api.sevices.userService import UserService

user_service = UserService()

class UserRegistrationView(APIView):

    """Register view."""
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    def post(self, request, format=None):
        result,status_code,msg = user_service.register(request, format=None)
        return Response({
                    "data":result,
                    "code":status_code,
                    "message":msg
        })
    
class UserLoginView(APIView):

    """Register view."""
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    def post(self, request, format=None):
        result,status_code,msg = user_service.login(request, format=None)
        return Response({
                    "data":result,
                    "code":status_code,
                    "message":msg
        })
    

class UserVerificationView(APIView):
    def post(self, request, format=None):
        result = user_service.verify_otp(request, format=None)
        return Response(result.data, status=result.data["code"])
    

class SendMailView(APIView):
    def post(self, request, format=None):
        result = user_service.send_mail(request, format=None)
        return Response(result.data, status=result.data["code"])
    
class GetUserView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    def get(self, request, format=None):
        result = user_service.get(request, format=None)
        return Response(result.data, status=result.data["code"])
            

class UpdateUserView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    def get(self, request, format=None):
        result = user_service.update(request, format=None)
        return Response(result.data, status=result.data["code"])
            