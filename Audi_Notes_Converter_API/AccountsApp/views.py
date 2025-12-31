from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)

from ActivityLog.utils import log_activity


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            log_activity(
                request=request,
                user=None,
                action="REGISTER",
                details="Registration failed (validation error)",
                status="failed",
            )
            serializer.is_valid(raise_exception=True)

        user = serializer.save()

        log_activity(
            request=request,
            user=user,
            action="REGISTER",
            details=f"User registered with email {user.email}",
            status="success",
        )

        return Response(
            {
                "message": "User registered successfully",
                "User": {
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            log_activity(
                request=request,
                user=None,
                action="LOGIN",
                details="Login failed (invalid credentials)",
                status="failed",
            )
            serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = validated_data["user"]

        log_activity(
            request=request,
            user=user,
            action="LOGIN",
            details="Login successful",
            status="success",
        )

        return Response(
            {
                "message": "Login successful",
                "token": {
                    "refresh": validated_data["refresh"],
                    "access": validated_data["access"],
                },
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        log_activity(
            request=request,
            user=request.user,
            action="LOGOUT",
            details="User logged out",
            status="success",
        )

        return Response(
            {"message": "Successfully logged out"},
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            log_activity(
                request=request,
                user=request.user,
                action="CHANGE_PASSWORD",
                details="Password change failed (validation error)",
                status="failed",
            )
            serializer.is_valid(raise_exception=True)

        serializer.save()

        log_activity(
            request=request,
            user=request.user,
            action="CHANGE_PASSWORD",
            details="Password changed successfully",
            status="success",
        )

        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            log_activity(
                request=request,
                user=None,
                action="PASSWORD_RESET_REQUEST",
                details="Password reset request failed",
                status="failed",
            )
            serializer.is_valid(raise_exception=True)

        results = serializer.save()

        log_activity(
            request=request,
            user=None,
            action="PASSWORD_RESET_REQUEST",
            details=f"Password reset requested for {request.data.get('email')}",
            status="success",
        )

        return Response(results, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            log_activity(
                request=request,
                user=None,
                action="PASSWORD_RESET_CONFIRM",
                details="Password reset confirmation failed",
                status="failed",
            )
            serializer.is_valid(raise_exception=True)

        serializer.save()

        log_activity(
            request=request,
            user=None,
            action="PASSWORD_RESET_CONFIRM",
            details="Password reset confirmed successfully",
            status="success",
        )

        return Response(
            {"message": "Password has been reset successfully"},
            status=status.HTTP_200_OK,
        )


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        if not serializer.is_valid():
            log_activity(
                request=request,
                user=request.user,
                action="PROFILE_UPDATE",
                details="Profile update failed",
                status="failed",
            )
            serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        log_activity(
            request=request,
            user=request.user,
            action="PROFILE_UPDATE",
            details="Profile updated successfully",
            status="success",
        )

        return Response(
            {
                "message": "Profile update successfully",
                "user": {
                    "username": instance.username,
                    "email": instance.email,
                    "first_name": instance.first_name,
                    "last_name": instance.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )