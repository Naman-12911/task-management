from django.urls import path
from .views import *
urlpatterns = [
    path('register/', Register.as_view(),name="Register"),
    path('login/', Login.as_view(), name='Login'),
    path('profile/',userData.as_view(),name="profile"),
    path('update-profile/',update_profile.as_view(),name="update_profile"),
    path('all-user/',AllUserAPIview.as_view(),name="AllUserAPIview"),
]
