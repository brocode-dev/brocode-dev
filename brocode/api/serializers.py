"""
Serializer for the user API View.
"""

from api.models import User

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
# from rest_framework.validators import UniqueValidator
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email, EmailValidator
from .utils.password_validate import password_check
class UserSerializer(serializers.ModelSerializer):
	
    class Meta:
        model =User
        fields = ['email', 'password', 'name']

	
    def validate(self, attr):
          if not password_check(attr['password'])[0]:
              raise serializers.ValidationError(password_check(attr['password'])[1])
          if User.objects.filter(email = attr['email']):
              raise serializers.ValidationError("Email exists!")
          return attr
    
    

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],name=validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
 
    

# class VerifyOTPSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField()
