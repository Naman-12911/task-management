from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

class CustomUserThrottle(UserRateThrottle):
    rate = '10/minute'

#throttle_classes = [CustomUserThrottle]
