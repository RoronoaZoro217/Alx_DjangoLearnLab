from django.db import models
from django.conf import settings

# Example: if you have books in this app
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='books'
    )

    def __str__(self):
        return self.title

