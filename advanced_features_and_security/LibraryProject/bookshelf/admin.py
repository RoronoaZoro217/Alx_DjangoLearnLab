from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.
    """
    model = CustomUser
    
    # Fields to display in the admin list view
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active']
    
    # Fields to filter by in the admin list view
    list_filter = ['is_staff', 'is_active', 'is_superuser', 'date_joined']
    
    # Fields to search in the admin
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    # Ordering in the admin list view
    ordering = ['username']
    
    # Fieldsets for the user detail/edit page
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Fieldsets for the add user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_photo', 'is_staff', 'is_active')
        }),
    )


# Register the CustomUser model with the CustomUserAdmin configuration
admin.site.register(CustomUser, CustomUserAdmin)