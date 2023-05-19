from rest_framework import status
from rest_framework.response import Response
from api.serializers import UserSerializer, VerifyOTPSerializer
from django.contrib.auth import get_user_model

from .userBaseService import UserBaseService
from api.email import send_otp_via_email

from api.models import User

class UserService(UserBaseService):
    def __init__(self):
        pass

    def register(self, request, format=None):
        """User Registeration."""
        try:
            # breakpoint()
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return serializer.data, status.HTTP_200_OK,'Register Successfully'
            else:
                return serializer.errors, status.HTTP_400_BAD_REQUEST,'Register Failed'
        
        except Exception as e:
            print(e)


    def verifyOTP(self, request, format=None):
        try: 
            serializer = VerifyOTPSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                user = User.objects.filter(email = email)
                if not user:
                    return Response({
                        "data":{},
                        "code":status.HTTP_400_BAD_REQUEST,
                        "message":"Invalid email!"
                    })
                elif not user[0].otp == otp:
                    return Response({
                        "data":{},
                        "code":status.HTTP_400_BAD_REQUEST,
                        "message":"Invalid OTP!"
                    })
                user=user.first()
                user.is_verified = True
                user.save()
                return Response({
                        "data":{},
                        "code":status.HTTP_200_OK,
                        "message":"User verifid!"
                    })
            return Response({
                        "data":serializer.errors,
                        "code":status.HTTP_400_BAD_REQUEST,
                        "message":"Something went wrong!"
            })
        
        except Exception as e:
            print(e)
                    
