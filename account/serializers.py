from .models import User
import logging
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.models import User
import re
from django.db import transaction
logger = logging.getLogger(__name__)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ['email', 'phone_no', 'first_name', 'last_name', 'password', 'admin','user',]
    def validate_phone_no(self, value):
        # Check if phone_no contains only digits
        if not re.match(r'^\+?\d+$', value):
            raise serializers.ValidationError("Phone number must contain only digits.")
        if not (10 <= len(value) <= 13):
            raise serializers.ValidationError("Phone number must be between 10 and 13 digits.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['phone_no', 'password', 'tokens', 'email', 'user', 'id', 'first_name','last_name', 'admin']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
       
       
        if user.user:
            if user.check_password(password):
                user_type = 'user'
                return {
                    'email': user.email,
                    'user_type': user_type,
                    'tokens': user.tokens(),
                    'user': user.user,
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
        elif user.admin:
            user_type = 'admin'
            return {
                 'email': user.email,
                'user_type': user_type,
                'tokens': user.tokens(),
                "id": user.id,
                'admin': user.admin,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        else:
            raise AuthenticationFailed('Invalid authentication type')
        
class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name','id']