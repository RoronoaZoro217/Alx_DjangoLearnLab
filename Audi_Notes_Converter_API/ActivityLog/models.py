from django.db import models
from django.conf import settings

# Create your models here.
class ActivityLog(models.Model):
    STATUS_CHOICES = [
        ('success','Success'),('failed','Failed'),
    ]

    ACTION_MAX = 50

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs'
    )

    action = models.CharField(
        max_length=ACTION_MAX, help_text='Action keyword, e.g LOGIN, UPLOAD, DELETE'
    )

    details = models.TextField(
        blank=True,
        help_text='Additional details (JSON or Plain text)'
    )

    ip_address = models.GenericIPAddressField(
        null=True,blank=True
    )

    status = models.CharField(max_length=10,choices=STATUS_CHOICES)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    def __str__(self):
        user_display = self.user.email if self.user else 'Anonymous'
        return f"{self.timestamp} | {user_display} | {self.action} | {self.status}"
