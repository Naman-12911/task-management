from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Actions,Notifications
from .serializer import ActionsSerializers,NotificationsSerializers

class ActionsAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Actions, pk=pk)  # Use Django's shortcut

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_object(pk)
            serializer = ActionsSerializers(data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            data = Actions.objects.all()  # Removed is_published filter
            serializer = ActionsSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        current_user = request.user
        mutable_data = request.data.copy()

        mutable_data['assigned_by'] = current_user.id  # Ensure the correct field name

        serializer = ActionsSerializers(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        action = serializer.save()  # Save the action instance
        Notifications.objects.create(
        user_id=action.assigned_to,  # Notify the assigned user
        action_id=action,
        message=f"You have been assigned a new action: {action.heading}",
        is_read=False
    )

        return Response({
            'message': 'Action Created Successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def patch(self, request, pk=None, format=None):
        action_to_update = self.get_object(pk)

        serializer = ActionsSerializers(instance=action_to_update, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Action updated Successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class ActionsForUserAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Actions, pk=pk)  # Use Django's shortcut

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_object(pk)
            serializer = ActionsSerializers(data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            data = Actions.objects.filter(user = request.user)  # Removed is_published filter
            serializer = ActionsSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class NotificationsAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Actions, pk=pk)  # Use Django's shortcut

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_object(pk)
            serializer = NotificationsSerializers(data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            data = Notifications.objects.filter(user=request.user)
            serializer = NotificationsSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None, format=None):
        action_to_update = self.get_object(pk)

        serializer = NotificationsSerializers(instance=action_to_update, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Notifications updated Successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)