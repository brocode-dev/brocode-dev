from rest_framework import status
from rest_framework.response import Response
from api.serializers import RegistrationSerializer, LoginSerializer, UserGetUpdateSerializer
from django.contrib.auth import get_user_model

import jwt

from django.conf import settings
from datetime import datetime, timezone, timedelta

from api.utils import get_user_by_token

from .userBaseService import UserBaseService
from api.email import send_otp_via_email

from api.models import User, Otp

class UserService(UserBaseService):
    def __init__(self):
        pass

    def register(self, request, format=None):
        """User Registeration."""
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data, status.HTTP_200_OK,'Register Successfully'
            else:
                return serializer.errors, status.HTTP_400_BAD_REQUEST,'Register Failed'
    
        except Exception as e:
            return "", status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)

    def _generate_jwt_token(self, user):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': user.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    def login(self, request, format=None):
        """User Login."""
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user_details = serializer.data
                user = User.objects.get(email=user_details['email'])
                user_details['token'] = self._generate_jwt_token(user)
                return user_details, status.HTTP_200_OK,'Login Successfully!'
            else:
                return serializer.errors, status.HTTP_400_BAD_REQUEST,'Login Failed!'
    
        except Exception as e:
            return "", status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)

    def verify_otp(self, request, format=None):
        try: 
            if 'email' not in request.data or 'otp' not in request.data:
                return Response({
                    "data":{},
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"Email and OTP both fields are required."
                })
            email = request.data['email']
            otp = request.data['otp']
            breakpoint()
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
            return Response({
                    "data":{},
                    "code":status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": str(e)
                })
                    
    def send_mail(self, request, format=None):
        if 'email' not in request.data:
            return Response({
                "data":{},
                "code":status.HTTP_400_BAD_REQUEST,
                "message":"Email field is required."
            })
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
    
    def get(self, request, format=None):
        """Get User."""
        try:
            user_details = get_user_by_token(request)
            details_obj =  User.objects.get(pk=user_details["user_id"])
            serializer = UserGetUpdateSerializer(details_obj)
            if serializer:
                return Response({'data':serializer.data, 'code':status.HTTP_200_OK, 'message':'Successful!'})
            else:
                return Response({'data':None, 'code':status.HTTP_400_BAD_REQUEST, 'message':serializer.errors})
        except Exception as e:
            return Response({'data':None, 'code':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':str(e)})

    def update(self, request, format=None):
        """Update User."""
        try:
            data = request.user.get('user', {})
            serializer = UserGetUpdateSerializer(request.user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data, 'code':status.HTTP_200_OK, 'message':'Updated Successfully!'})
            else:
                return Response({'data':None, 'code':status.HTTP_400_BAD_REQUEST, 'message':serializer.errors})
        except Exception as e:
            return Response({'data':None, 'code':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':str(e)})
