from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.utils.translation import gettext_lazy  as _
from account.managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

# resgiter the user
AUTH_PROVIDERS = {'email': 'email'}

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_no = models.CharField(unique=True,null=True,max_length=13,blank=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    user = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email',))
    assign = models.BooleanField(default=True, blank=True, null=True)
    USERNAME_FIELD = 'email'
    objects = CustomUserManager() 
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
