from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profiles/',blank=True,null=True)

    followers = models.ManyToManyField('self',symmetrical=False,related_name='following',blank=True)
    
    def __str__(self):
        return self.get_full_name()
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
