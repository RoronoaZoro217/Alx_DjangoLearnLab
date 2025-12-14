from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse, Http404
import os

from .models import Document
from .serializers import (
    DocumentSerializer,
    DocumentUpdateSerializer,
    DocumentUploadSerializer
)

# Custom permission
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Prevent swagger crash
        if getattr(self, 'swagger_fake_view', False):
            return Document.objects.none()

        return Document.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentUploadSerializer
        elif self.action in ['update', 'partial_update']:
            return DocumentUpdateSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #DOWNLOAD ENDPOINT
    @action(detail=True, methods=['get'], url_path='download')  # ✅ STILL GET
    def download(self, request, pk=None):
        document = self.get_object()

        if not document.file:
            raise Http404("File not found")

        file_path = document.file.path

        #Ensure file exists on disk
        if not os.path.exists(file_path):
            raise Http404("File not found on disk")

        #FORCE DOWNLOAD
        response = FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(file_path)
        )

        return response
