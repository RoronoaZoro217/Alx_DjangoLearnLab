from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for handling user creation with additional fields.
    """
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a regular user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email) if email else None
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given username, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser with additional fields.
    """
    date_of_birth = models.DateField(
        null=True, 
        blank=True, 
        help_text="User's date of birth"
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text="User's profile photo"
    )
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
        # ✅ Added required custom permissions
        permissions = [
            ("can_view", "Can view restricted content"),
            ("can_create", "Can create objects"),
            ("can_edit", "Can edit objects"),
            ("can_delete", "Can delete objects"),
        ]
    
    def __str__(self):
        return self.username
    
    def get_age(self):
        """
        Calculate and return the user's age based on date_of_birth.
        """
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            age = today.year - self.date_of_birth.year
            
            if (
                today.month < self.date_of_birth.month or 
                (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day)
            ):
                age -= 1

            return age
        return None
