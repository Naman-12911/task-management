# from django.shortcuts import render
# from account.models import User
# from .models import TMC
# from rest_framework.permissions import AllowAny,IsAuthenticated
# from rest_framework import status
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from django.db.models import Q
# from .serializers import UserTMCSerializers,UserTMCLoginSerializer,UserTMCProfileSerializers
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# from rest_framework_simplejwt.exceptions import TokenError
# from django.contrib.auth import get_user_model

# class Register(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserTMCSerializers
#     # renderer_classes = (UserRenderer,)
#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         success_message = "TMC created successfully."
#         user = User.objects.get(email=user_data['email'])
#         return Response(user_data, status=status.HTTP_201_CREATED)
    
# # login apis
# class Login(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserTMCLoginSerializer
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class LogoutAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#             try:
#                 # Blacklist the refresh token
#                 refresh_token = request.data.get('refresh_token')
#                 if refresh_token:
#                     token = RefreshToken(refresh_token)
#                     token.blacklist()
#                 return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
# class userData(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         tmc = TMC.objects.get(user=request.user)
#         serializer = UserTMCProfileSerializers(tmc)
#         return Response(serializer.data)
#     def patch(self, request, *args, **kwargs):
#         tmc = TMC.objects.get(user=request.user)
#         user = tmc.user
#         user_data = {
#             'first_name': request.data.get('first_name'),
#             'last_name': request.data.get('last_name'),
#             'email': request.data.get('email'),
#             'phone_no': request.data.get('phone_no')
#         }

#         for field, value in user_data.items():
#             if value is not None:
#                 setattr(user, field, value)
#         user.save()  # Save the updated User instance
#         doctor_data = {key: value for key, value in request.data.items() if key not in user_data}
#         serializer = UserTMCProfileSerializers(tmc, data=doctor_data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()  # Save the updated Doctor instance
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class GetRefreshTokenFromAccessToken(APIView):
#     permission_classes = [IsAuthenticated] 
#     def post(self, request):
#         auth_header = request.headers.get('Authorization', None)
#         if not auth_header:
#             return Response({"detail": "Authorization header is missing."}, status=400)
#         if not auth_header.startswith('Bearer '):
#             return Response({"detail": "Invalid Authorization header format."}, status=400)
#         access_token = auth_header.split(' ')[1]
#         try:
#             decoded_access_token = AccessToken(access_token)
#             user_id = decoded_access_token.payload.get('user_id')
#             user = get_user_model().objects.get(id=user_id)
#             refresh_token = RefreshToken.for_user(user)
#             return Response({
#                 "refresh": str(refresh_token),
#                 "access": str(decoded_access_token)
#             }, status=200)
#         except TokenError as e:
#             return Response({"detail": str(e)}, status=400)