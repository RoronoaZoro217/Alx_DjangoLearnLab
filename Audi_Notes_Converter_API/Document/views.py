from rest_framework import viewsets, permissions, status
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

from ActivityLog.utils import log_activity

# Custom permission
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        allowed = obj.user == request.user

        if not allowed:
            log_activity(
                request=request,
                user=request.user,
                action="DOCUMENT_ACCESS_DENIED",
                details=f"Unauthorized access attempt to document ID {obj.id}",
                status="failed",
            )

        return allowed


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
        document = serializer.save(user=self.request.user)

        log_activity(
            request=self.request,
            user=self.request.user,
            action="DOCUMENT_UPLOAD",
            details=f"Document uploaded (ID {document.id})",
            status="success",
        )

    def perform_update(self, serializer):
        document = serializer.save()

        log_activity(
            request=self.request,
            user=self.request.user,
            action="DOCUMENT_UPDATE",
            details=f"Document updated (ID {document.id})",
            status="success",
        )

    def perform_destroy(self, instance):
        document_id = instance.id
        instance.delete()

        log_activity(
            request=self.request,
            user=self.request.user,
            action="DOCUMENT_DELETE",
            details=f"Document deleted (ID {document_id})",
            status="success",
        )

    # DOWNLOAD ENDPOINT
    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        document = self.get_object()

        if not document.file:
            log_activity(
                request=request,
                user=request.user,
                action="DOCUMENT_DOWNLOAD",
                details=f"Download failed: no file attached (ID {document.id})",
                status="failed",
            )
            raise Http404("File not found")

        file_path = document.file.path

        if not os.path.exists(file_path):
            log_activity(
                request=request,
                user=request.user,
                action="DOCUMENT_DOWNLOAD",
                details=f"Download failed: file missing on disk (ID {document.id})",
                status="failed",
            )
            raise Http404("File not found on disk")

        log_activity(
            request=request,
            user=request.user,
            action="DOCUMENT_DOWNLOAD",
            details=f"Document downloaded (ID {document.id})",
            status="success",
        )

        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(file_path),
        )