from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('read', '-timestamp')


class MarkNotificationReadView(generics.GenericAPIView):
    """
    Mark a specific notification as read.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notification_id, *args, **kwargs):
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

        notification.read = True
        notification.save()
        return Response({"detail": "Notification marked as read"}, status=status.HTTP_200_OK)