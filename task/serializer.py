from .models import Actions,Notifications
from rest_framework import serializers


class ActionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Actions
        fields = ['id','assigned_to','assigned_by','assigned_date','due_date','status','heading','description']


class NotificationsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = "__all__"