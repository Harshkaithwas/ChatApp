from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save()
        return user

class Account(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=40, unique=True, null=True)
    otp = models.CharField(max_length=6, validators=[MinLengthValidator(6)], default=None, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    age = models.PositiveIntegerField(null=True, blank=True)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()
    interests = models.ManyToManyField('self', symmetrical=False, through='UserInterest', related_name='related_to')
    friends = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='user_friends')

    def __str__(self):
        return self.email

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token)
        }

    # Customize additional fields and methods as needed for your chat application

class UserInterest(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_interests')
    interest = models.CharField(max_length=255)
    preference_score = models.PositiveIntegerField(
        default=50,
        validators=[MinValueValidator(1), MaxValueValidator(999)]  # Valid range is 1 to 999
    )

    def __str__(self):
        return f"{self.interest} (Preference: {self.preference_score})"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_requests')
    accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"From {self.from_user} to {self.to_user}"
