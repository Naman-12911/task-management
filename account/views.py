from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView


# Create your views here.
class Register(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)
    
class Login(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        #user_instance = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class userData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserRegistrationSerializer(self.request.user)
        return Response(serializer.data)

# update the user details
class update_profile(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRegistrationSerializer
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)