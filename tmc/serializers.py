from .models import TMC
from account.models import User
from rest_framework import serializers
from django.db.models import Q
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth

class TMCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TMC
        fields = [
          'state','village','work_experience','qualification','pincode','photo','document'
        ]
    
# login serializers
class UserTMCLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        try:
            user = User.objects.get(email=obj['email'])
            return {
                # 'refresh': user.tokens()['refresh'],
                'access': user.tokens()['access']
            }
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')

    class Meta:
        model = User
        fields = [
          'email', 'tmc_operator_user', 'id','tokens','password'
        ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        # Fetch the user by email
        filtered_user_by_email = User.objects.filter(email=email).first()

        if not filtered_user_by_email:
            raise AuthenticationFailed('Invalid credentials, try again')

        # Check the authentication provider
        if filtered_user_by_email.auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email.auth_provider
            )

        user = auth.authenticate(email=email, password=password)

        # Ensure the user is active and exists
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        # Check if the user has a related doctor profile
        if user.tmc_operator_user:
            tmc = user.tmc  # Assuming 'user.doctor' gives the Doctor instance
            if tmc and user.check_password(password):
                return {
                    'email': user.email,
                    'tmc_operator_user': user.tmc_operator_user,
                    'id': user.id,
                    'tokens': user.tokens(),  # Tokens are added at the top level
                }
        else:
            raise AuthenticationFailed('User does not have a doctor profile')

        # Return the final token and user details
        return {
            'email': user.email,
            'tokens': user.tokens()
        }


class UserTMCProfileSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')  
    last_name = serializers.CharField(source='user.last_name')    
    email = serializers.EmailField(source='user.email')       
    phone_no = serializers.CharField(source='user.phone_no')     
    class Meta:
        model = TMC
        fields = [
           'email','phone_no','first_name','last_name','state',
           'village','work_experience','qualification','pincode','photo','document'
        ]
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance