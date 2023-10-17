from rest_framework import serializers
from accounts.models import *
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import random
from django.core.validators import MinLengthValidator
import string

from django.contrib.auth import get_user_model
User = get_user_model()


def validate_password(value):
    if len(value) < 6:
        raise ValidationError("Password must be at least 6 characters long.")
    allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_")
    if not set(value).issubset(allowed_characters):
        raise ValidationError("Password can only include a-z, A-Z, 0-9, @, _.")




class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, required=True)

    def validate_email(self, email):
        if not Account.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is not registered.")
        return email

    def validate_otp(self, otp):
        if len(otp) != 6 or not otp.isdigit():
            raise serializers.ValidationError("OTP must be a 6-digit number.")
        return otp


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def generate_otp(self, length=6):
        return ''.join(random.choices(string.digits, k=length))

    def send_verification_email(self, email, otp):
        subject = 'Email Verification OTP'
        message = f'Your OTP for email verification is: {otp}'
        from_email = 'rc261121@example.com'  # Set your from email address here
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list) 

    def save(self, **kwargs):
        email = self.validated_data['email']
        otp = self.generate_otp()
        self.send_verification_email(email, otp)

        return {'email': email, 'otp': otp}


from rest_framework import serializers
from .models import Account
import random
import string
from django.core.mail import send_mail

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not Account.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is not registered.")
        return email

    def resend_otp(self, email):
        # Generate a new OTP
        otp = ''.join(random.choices(string.digits, k=6))

        # Update the OTP in the model
        user = Account.objects.get(email=email)
        user.otp = otp
        user.save()

        # Send the new OTP via email
        subject = 'Resent OTP for Email Verification'
        message = f'Your new OTP for email verification is: {otp}'
        from_email = 'rc261121@example.com'  # Set your from email address here
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        return {"message": "OTP resent for verification.",'email': email, 'otp': otp}


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    otp = serializers.CharField(max_length=6, validators=[MinLengthValidator(6)], write_only=True, required=False)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'confirm_password', 'otp']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, email):
        if Account.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already in use.")
        return email

    def save(self, **kwargs):
        email = self.validated_data['email']
        username = self.validated_data['username']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        otp = self.validated_data.get('otp')


        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match'})

        if not otp:
            # Use the EmailVerificationSerializer to send verification email and generate OTP
            email_serializer = EmailVerificationSerializer(data={'email': email})
            email_serializer.is_valid(raise_exception=True)
            validated_data = email_serializer.save()
            otp = validated_data['otp']

        account = Account(
            email=email,
            username=username,
            is_verified=False
        )

        account.set_password(password)
        account.otp = otp
        account.save()

        return account


class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = ['id','interest', 'preference_score']


class UpdateInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = ['id','interest', 'preference_score']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'accepted']



class AccountSerializer(serializers.ModelSerializer):
    interests = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'username', 'age', 'interests']

    def get_interests(self, obj):
        interests_data = obj.user_interests.all()
        interests_dict = {interest.interest: interest.preference_score for interest in interests_data}
        return interests_dict
    


