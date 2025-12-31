from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import ActivityLog
from .serializers import ActivityLogSerializer

# Create your views here.
class ActivityLogListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logs = ActivityLog.objects.all().order_by("-timestamp")
        serializer = ActivityLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserActivityLogView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        logs = ActivityLog.objects.filter(user_id=user_id).order_by("-timestamp")
        serializer = ActivityLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
