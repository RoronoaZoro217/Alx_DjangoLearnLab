from django.db import models
from django.conf import settings
import os

# Create your models here.
User = settings.AUTH_USER_MODEL

def document_upload_path(instance, filename):
    #store documents per user & file type
    extension = filename.split('.')[-1].lower()

    #media/documents/user_<id>/<pdf|docx>/<filename>
    return f"documents/user_{instance.user_id}/{extension}/{filename}"

class Document(models.Model):
    FILE_TYPE_CHOICES = (
        ('pdf','PDF'),('docx','DOCX'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='documents')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=document_upload_path,null=True,blank=True)
    file_type = models.CharField(max_length=10,choices=FILE_TYPE_CHOICES)
    file_size = models.BigIntegerField(help_text='File size in bytes')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.file_type})"
    
    def delete(self, *args, **kwargs):
        #Ensure file is deleted from storage when the document is deleted
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)

        return super().delete(*args, **kwargs)
