from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import secrets

# Create your models here.
class CustomUser(AbstractUser):
    REQUIRED_FIELDS = ['email','first_name','last_name']

class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='password_reset_tokens')
    token = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reset token for {self.user.username}"
    
    @staticmethod
    def generate_token():
        #generate a secure random token
        return secrets.token_urlsafe(32)
    
    def is_valid(self):
        #validate the token
        return not self.is_used and timezone.now() < self.expires_at
    
    def save(self,*args, **kwargs):
        if not self.token:
            self.token = self.generate_token()

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(seconds=300)

        super().save(*args, **kwargs)
