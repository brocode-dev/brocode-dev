"""
User Views.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.sevices.userService import UserService

user_service = UserService()

class UserRegistrationView(APIView):

    """Register view."""

    def post(self, request, format=None):
        result,status_code,msg = user_service.register(request, format=None)
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
            