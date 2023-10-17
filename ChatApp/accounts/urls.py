from django.urls import path
from . import views
from accounts.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView, TokenBlacklistView


urlpatterns = [
    path('otp_verification/', OTPVerificationView.as_view(), name='otp_verification'),
    path('resend_otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('sign_up/', views.RegistrationView.as_view(), name='registration'),
    path('sign_in/', views.SignInView.as_view(), name='login'),
    path('sign_out/', views.SignOutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/bl/', TokenBlacklistView.as_view(), name='token_bl'),#can use to logout




]
