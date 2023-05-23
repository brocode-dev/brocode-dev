from rest_framework import status
from rest_framework.response import Response
from api.serializers import UserSerializer
from django.contrib.auth import get_user_model

from datetime import datetime, timezone

from .userBaseService import UserBaseService
from api.email import send_otp_via_email

from api.models import User, Otp

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
                # send_otp_via_email(serializer.data['email'])
                return serializer.data, status.HTTP_200_OK,'Register Successfully'
            else:
                return serializer.errors, status.HTTP_400_BAD_REQUEST,'Register Failed'
        
        except Exception as e:
            print(e)


    def verifyOTP(self, request, format=None):
        try: 
            email = request.data['email']
            otp = request.data['otp']
            user = User.objects.filter(email = email)
            if not user:
                return Response({
                    "data":{},
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"Invalid email!"
                })
            latest_otp=user.first().otp_set.all().order_by("-created_at")[0]
            time = datetime.now(timezone.utc) - latest_otp.created_at

            if ((time.seconds % 3600) // 60) > 5 :
                latest_otp.is_expire=True
                latest_otp.save()
            
            if latest_otp.is_expire :

                return Response({
                    "data":{},
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"OTP expire!"
                }) 
            elif not latest_otp.otp == otp:
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
                    "message":"Email varified!"
                })
        except Exception as e:
            print(e)
                    
    def sendMail(self, request, format=None):
        email = request.data['email']
        user = User.objects.filter(email=email)
        if not user:
            return Response({
                "data":{},
                "code":status.HTTP_400_BAD_REQUEST,
                "message":"Invalid email!"
            })
        send_otp_via_email(email)
        
        return Response({
                "data":{},
                "code":status.HTTP_200_OK,
                "message":"OTP sent to your email successfully!"
            })
