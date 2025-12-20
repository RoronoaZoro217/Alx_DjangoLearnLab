from rest_framework import serializers
from .models import AudioFile
from Document.models import Document


class AudioFileSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for audio metadata
    """
    document_id = serializers.IntegerField(
        source="document.id",
        read_only=True
    )
    document_title = serializers.CharField(
        source="document.title",
        read_only=True
    )

    class Meta:
        model = AudioFile
        fields = [
            "id",
            "document_id",
            "document_title",   # ✅ added
            "audio_file",
            "duration",
            "created_at",
        ]
        read_only_fields = fields

class AudioGenerateSerializer(serializers.Serializer):
    """
    Serializer for generating audio
    """
    document_id = serializers.IntegerField(read_only=True)
    message = serializers.CharField(read_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        document_id = self.context.get("document_id")

        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise serializers.ValidationError("Document not found")

        if document.user != request.user:
            raise serializers.ValidationError(
                "You do not have permission to generate audio for this document"
            )

        if not document.file:
            raise serializers.ValidationError(
                "Document has no file attached"
            )

        attrs["document"] = document
        return attrs
