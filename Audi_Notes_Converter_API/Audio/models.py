from django.db import models
from django.conf import settings
from Document.models import Document
import os

# Create your models here.
def audio_upload_path(instance, filename):
    #store generated audio per user & document
    #media/audio/user_<id>/document_<id>/<filename>.mp3
    return f"audio/user_{instance.document.user_id}/document_{instance.document.id}/{filename}"

class AudioFile(models.Model):
    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        related_name='audio'
    )

    audio_file = models.FileField(
        upload_to=audio_upload_path
    )

    file_size = models.BigIntegerField(
        help_text='Audio file size bytes'
    )

    duration = models.IntegerField(
        null=True,
        blank=True,
        help_text='Audio duration in seconds'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Audio for document: {self.document.title}"
    
    def delete(self, *args,**kwargs):
        #ensure audio file is deleted from storage when record is deleted
        if self.audio_file and os.path.isfile(self.audio_file.path):
            os.remove(self.audio_file.path)

        super().delete(*args,**kwargs)
