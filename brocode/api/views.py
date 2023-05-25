"""
User Views.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .utils.renderers import UserJSONRenderer

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
        result = user_service.verifyOTP(request, format=None)
        return Response(result.data, status=result.data["code"])
    

class SendMailView(APIView):
    def post(self, request, format=None):
        result = user_service.sendMail(request, format=None)
        return Response(result.data, status=result.data["code"])
            