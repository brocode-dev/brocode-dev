"""
Serializer for the user API View.
"""

from api.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .utils.password_validate import password_check


class RegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model =User
        fields = ['email', 'password', 'username', 'token']

	
    def validate(self, attr):
          if not password_check(attr['password'])[0]:
              raise serializers.ValidationError(password_check(attr['password'])[1])
          if User.objects.filter(email = attr['email']):
              raise serializers.ValidationError("Email exists!")
          return attr
    
    

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    # token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        # breakpoint()

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            # 'token': user.token
        }


class UserGetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['email', 'password', 'username', 'token']
        read_only_fields = ('token',)
	
    # def validate(self, attr):
    #       if not password_check(attr['password'])[0]:
    #           raise serializers.ValidationError(password_check(attr['password'])[1])
    #       return attr
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        if password is not None:
            instance.set_password(password)
        
        instance.save()

        return instance