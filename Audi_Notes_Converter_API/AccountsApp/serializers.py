from .models import CustomUser, PasswordResetToken
from rest_framework import serializers
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError as DjangoValidationError
from django.conf import settings
from django.core.mail import send_mail


class UserRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['url','username','email','first_name','last_name','password']

    def validate_email(self, value):
        #validate email format
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError('Enter a valid email address.')
            
        #Validate the email existance
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exist')
            
        #limit email domains to: 'gmail.com','outlook.com','outlook.co.za','hotmail.com','live.com',
        domain = value.split('@')[1].lower()
        if domain not in settings.ALLOWED_EMAIL_DOMAINS:
            raise serializers.ValidationError(f"Only the following email providers are allowed: {', '.join(settings.ALLOWED_EMAIL_DOMAINS)}")
            
        return value.lower()
        
    def validate_password(self, value):
        validate_password(value)

        return value
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        """
        Validate user credentials (username or email) and return tokens
        """
        username_or_email = data.get('username_or_email')
        password = data.get('password')
        
        # Check if fields are provided
        if not username_or_email:
            raise serializers.ValidationError('Username or email is required.')
        
        if not password:
            raise serializers.ValidationError('Password is required.')
        
        # Try to find user by username or email
        user = None
        
        # Check if input is an email
        if '@' in username_or_email:
            try:
                user_obj = CustomUser.objects.get(email=username_or_email.lower())
                # Authenticate using username (since Django's authenticate expects username)
                user = authenticate(username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                pass
        else:
            # Authenticate using username
            user = authenticate(username=username_or_email, password=password)
        
        if user is None:
            raise serializers.ValidationError('Invalid credentials.')
        
        if not user.is_active:
            raise serializers.ValidationError('This account is inactive.')
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        #Validate and blacklist the refresh token
        refresh_token = data.get('refresh')

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError('Invalid or expired token')
        
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True,required=True)
    new_password= serializers.CharField(write_only=True,required=True,min_length=8)
    confirm_password = serializers.CharField(write_only=True,required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user

        #verify the current password
        if not user.check_password(value):
            raise serializers.ValidationError('The current password is incorrect')
        
        return value
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, data):
        #validate password confirmation
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {
                    'confirm_password': 'New passwords do not match'
                }
            )
        
        #validate password repetition
        if data['current_password'] == data['new_password']:
            raise serializers.ValidationError(
                {
                    'new_password': 'New and current password can not be the same'
                }
            )
        
        return data
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

        return user
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        #validate email format
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError('Enter a valid email address')
        return value
    
    def save(self):
        #generate token & send email
        email = self.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)

            #Invalidate any existing unused tokens for the curren tuser
            PasswordResetToken.objects.filter(user=user,is_used=False).update(is_used=True)

            reset_token = PasswordResetToken.objects.create(user=user)
            #send email
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token.token}"

            subject = "Password Reset Request"
            message = f"""
                    Hello {user.first_name or user.username},

                    Click the link below to reset your password
                    {reset_url}

                    This link will expire in 5 minutes.
                    If you didn't request the reset, please ignore this email.

                    Best regards,
                    The team
                    """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except CustomUser.DoesNotExist:
            pass

        return {
            'message': 'If your email is registered, you will receive the reset link'
        }
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True,required=True,min_length=8)
    confirm_password = serializers.CharField(write_only=True,required=True)

    def validate_token(self, value):
        #validate the existance of the token
        try:
            reset_token = PasswordResetToken.objects.get(token=value)

            if not reset_token.is_valid():
                raise serializers.ValidationError('Link expired or already used')
            
            self.context['reset_token'] = reset_token
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError('Invalid reset token')
        
        return value
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {
                    'confirm_password': 'Passwords do not match'
                }
            )
        return data
    
    def save(self):
        #reset user's password & mark token used
        reset_token = self.context['reset_token']
        user = reset_token.user

        #update 
        user.set_password(self.validated_data['new_password'])
        user.save()

        #mark the reset link as used
        reset_token.is_used = True
        reset_token.save()

        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','first_name','last_name','date_joined','last_login']
        read_only_field = ['id','username','email','date_joined','last_login']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name']

        def validate_email(self, value):
            #validate email format
            try:
                validate_email(value)
            except DjangoValidationError:
                raise serializers.ValidationError('Enter a valid email address')
            
            user = self.context['request'].user

            if CustomUser.objects.filter(email=value).exclude(id=user.id).exists():
                raise serializers.ValidationError('A user with this email already exists')
            
            #validate allowed email domains
            domain = value.split('@')[1].lower()
            if domain not in settings.ALLOWED_EMAIL_DOMAINS:
                raise serializers.ValidationError(
                    f"Only the following email providers are allowed: {', '.join(settings.ALLOWED_EMAIL_DOMAINS)}"
                )
            return value.lower()
