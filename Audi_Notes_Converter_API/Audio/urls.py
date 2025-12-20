from django.urls import path
from .views import (
    AudioMetadataView,
    AudioGenerateView,
    AudioDownloadView,
    AudioDeleteView,
)

urlpatterns = [
    # Get audio metadata for a document
    path('<int:document_id>/', AudioMetadataView.as_view(), name='audio-metadata'),

    # Generate audio (if not exists)
    path('<int:document_id>/generate/', AudioGenerateView.as_view(), name='audio-generate'),

    # Download audio file
    path('<int:document_id>/download/', AudioDownloadView.as_view(), name='audio-download'),

    # Delete audio file
    path('<int:document_id>/delete/', AudioDeleteView.as_view(), name='audio-delete'),
]
