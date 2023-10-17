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

    path('get_interests/', UserInterestView.as_view(), name='get_interests'),
    path('get_interests/<int:pk>/', views.UpdateInterestView.as_view(), name='update-user-interest'),

    path('friend_requests/', FriendRequestListView.as_view(), name='friend_requests'),
    path('friend_requests/<int:pk>/', FriendRequestDetailView.as_view(), name='accept_reject_friend_request'),


    path('friends_list/', ListUserFriendsView.as_view(), name='list_user_friends'),
    path('load_users/', LoadUsersViewSet.as_view(), name='load_users'),#for loading users from data 
    path('friend_recommendations/', FriendRecommendationsView.as_view(), name='friend_recommendations'),

]
