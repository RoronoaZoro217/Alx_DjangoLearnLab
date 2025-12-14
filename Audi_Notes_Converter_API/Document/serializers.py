from rest_framework import serializers
from .models import Document
import os

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'description',
            'file_type',
            'file_size',
            'uploaded_at',
            'updated_at',
        ]
        read_only_fields = ['id']


class DocumentUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'description',
            'file',
        ]
        read_only_fields = ['id']

    def validate_file(self, file):
        # validate file size (10MB max)
        max_size = 10 * 1024 * 1024
        if file.size > max_size:
            raise serializers.ValidationError("File size must not exceed 10MB")

        # validate file extension
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ['.pdf', '.docx']:
            raise serializers.ValidationError("Only PDF and DOCX files are allowed")

        return file

    def create(self, validated_data):
        uploaded_file = validated_data.get('file')

        # Ownership should be set in the ViewSet (perform_create)
        file_extension = os.path.splitext(uploaded_file.name)[1].lower().replace('.', '')

        validated_data['file_type'] = file_extension
        validated_data['file_size'] = uploaded_file.size

        #DRF handle object creation
        #Prevents duplication and keeps consistency
        return super().create(validated_data)

class DocumentUpdateSerializer(serializers.ModelSerializer):
    # Updating document metadata only
    class Meta:
        model = Document
        fields = ['title', 'description']
