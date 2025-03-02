from django.db import models
from account.models import BaseModel,User
from django.conf import settings

class TMC(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    state = models.CharField(max_length=100,null=True,blank=True)
    village = models.CharField(max_length=100,null=True,blank=True)
    work_experience = models.CharField(max_length=100,null=True,blank=True)
    qualification = models.CharField(max_length=100,null=True)
    pincode = models.IntegerField(null=True,blank=True)
    photo = models.ImageField(null=True,blank=True,upload_to=f"{settings.AWS_LOCATION}tmc/photos/")
    document = models.FileField(null=True,blank=True,upload_to=f"{settings.AWS_LOCATION}tmc/photos/")