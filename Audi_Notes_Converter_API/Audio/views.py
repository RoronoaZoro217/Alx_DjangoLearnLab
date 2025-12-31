import os
import tempfile

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.http import FileResponse, Http404

from gtts import gTTS
import pdfplumber
from docx import Document as DocxDocument

from .models import AudioFile
from .serializers import AudioFileSerializer, AudioGenerateSerializer
from Document.models import Document

from ActivityLog.utils import log_activity

# Helper functions
def extract_text_from_pdf(file_path):
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n\n".join(text)

def extract_text_from_docx(file_path):
    doc = DocxDocument(file_path)
    return "\n\n".join(
        [para.text for para in doc.paragraphs if para.text.strip()]
    )

def extract_text(document):
    if document.file_type == "pdf":
        return extract_text_from_pdf(document.file.path)
    elif document.file_type == "docx":
        return extract_text_from_docx(document.file.path)
    return ""

# Views
class AudioMetadataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, document_id):
        try:
            document = Document.objects.get(
                id=document_id, user=request.user
            )
            audio = AudioFile.objects.get(document=document)

            log_activity(
                request=request,
                user=request.user,
                action="AUDIO_METADATA",
                details=f"Fetched audio metadata (Document ID {document.id})",
                status="success",
            )

        except Document.DoesNotExist:
            log_activity(
                request=request,
                user=request.user,
                action="AUDIO_METADATA",
                details=f"Document not found (ID {document_id})",
                status="failed",
            )
            raise Http404("Document not found")

        except AudioFile.DoesNotExist:
            return Response(
                {"detail": "Audio not generated yet"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AudioFileSerializer(audio)
        return Response(serializer.data)

class AudioGenerateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, document_id):
        serializer = AudioGenerateSerializer(
            data={},
            context={"request": request, "document_id": document_id},
        )
        serializer.is_valid(raise_exception=True)
        document = serializer.validated_data["document"]

        try:
            audio = AudioFile.objects.get(document=document)
            if audio.audio_file:
                log_activity(
                    request=request,
                    user=request.user,
                    action="AUDIO_GENERATE",
                    details=f"Audio already exists (Document ID {document.id})",
                    status="success",
                )
                return Response(
                    {"message": "Audio already exists"},
                    status=status.HTTP_200_OK,
                )
        except AudioFile.DoesNotExist:
            audio = AudioFile(document=document)

        text = extract_text(document)
        if not text.strip():
            log_activity(
                request=request,
                user=request.user,
                action="AUDIO_GENERATE",
                details=f"No readable text found (Document ID {document.id})",
                status="failed",
            )
            return Response(
                {"detail": "No readable text found in document"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tts = gTTS(text=text, lang="en")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                tts.save(temp_audio.name)
                temp_audio_path = temp_audio.name

            filename = f"{document.title.replace(' ', '_')}.mp3"

            with open(temp_audio_path, "rb") as f:
                audio.audio_file.save(filename, f, save=False)

            audio.file_size = os.path.getsize(temp_audio_path)
            audio.save()

            os.remove(temp_audio_path)

            log_activity(
                request=request,
                user=request.user,
                action="AUDIO_GENERATE",
                details=f"Audio generated (Document ID {document.id})",
                status="success",
            )

            return Response(
                {"message": "Audio generated successfully"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            log_activity(
                request=request,
                user=request.user,
                action="AUDIO_GENERATE",
                details=f"Generation failed (Document ID {document.id}): {str(e)}",
                status="failed",
            )
            raise

class AudioDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, document_id):
        try:
            document = Document.objects.get(
                id=document_id, user=request.user
            )
            audio = AudioFile.objects.get(document=document)

            log_activity(
                request=request,
                user=request.user,
                action="AUDIO_DOWNLOAD",
                details=f"Audio downloaded (Document ID {document.id})",
                status="success",
            )

        except (Document.DoesNotExist, AudioFile.DoesNotExist):
            log_activity(
                request=request,
                user=request.user,
                action="AUDIO_DOWNLOAD",
                details=f"Audio not found (Document ID {document_id})",
                status="failed",
            )
            raise Http404("Audio not found")

        return FileResponse(
            audio.audio_file.open("rb"),
            as_attachment=True,
            filename=os.path.basename(audio.audio_file.name),
        )

class AudioDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, document_id):
        try:
            document = Document.objects.get(
                id=document_id, user=request.user
            )
            audio = AudioFile.objects.get(document=document)

            audio.audio_file.delete(save=False)
            audio.delete()

            log_activity(
                request=request,
                user=request.user,
                action="AUDIO_DELETE",
                details=f"Audio deleted (Document ID {document.id})",
                status="success",
            )

        except (Document.DoesNotExist, AudioFile.DoesNotExist):
            log_activity(
                request=request,
                user=request.user,
                action="AUDIO_DELETE",
                details=f"Audio delete failed (Document ID {document_id})",
                status="failed",
            )
            raise Http404("Audio file not found")

        return Response(
            {"message": "Audio file deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )