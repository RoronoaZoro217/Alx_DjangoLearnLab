from django.urls import path
from .views import UserRegistrationView, LoginView, LogoutView, ChangePasswordView,PasswordResetRequestView, PasswordResetConfirmView, UserProfileView, UserProfileUpdateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register/',UserRegistrationView.as_view(),name='user-registration'),
    path('auth/login/',LoginView.as_view(),name='user-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/logout/', LogoutView.as_view(), name='user-logout'),
    path('auth/change-password/',ChangePasswordView.as_view(),name='change-password'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    path('auth/profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
]