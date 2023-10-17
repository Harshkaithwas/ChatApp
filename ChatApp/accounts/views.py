from accounts.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Account
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action

import json
from random import randint


from django.contrib.auth import login

class RegistrationView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            email = request.data.get("email")
            password = request.data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)  # Log the user in after registration

                response_data = {
                    'message': 'Your Account Has Been Registered Successfully',
                    'user_id': user.id  # Include the user ID in the response
                }

                return Response(response_data, status=status.HTTP_201_CREATED)

            else:
                data = {'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        else:
            data = {'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)




class OTPVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response({"message": "Invalid email address"}, status=status.HTTP_404_NOT_FOUND)

            if user.is_verified:
                return Response({"message": "User is already verified."}, status=status.HTTP_400_BAD_REQUEST)

            if user.otp == otp:
                user.is_verified = True
                user.save()
                return Response({"message": "OTP verification successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResendOTPView(APIView):
    serializer_class = ResendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            response_data = serializer.resend_otp(email)
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SignInView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        account = Account.objects.filter(email=email)

        if account.exists():
            if (email and password):
                user = authenticate(email=email, password=password)

                if user is not None:
                    if user.is_verified:
                        user.is_online = True
                        user.save()
                        refresh = RefreshToken.for_user(user)
                        user_id = user.id  # Get the user ID

                        response = {
                            'success': True,
                            'status code': status.HTTP_200_OK,
                            'message': 'User logged in successfully',
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'user_id': user_id  # Include the user ID in the response
                        }
                        status_code = status.HTTP_200_OK
                        return Response(response, status=status_code)
                    else:
                        response = {
                            'success': False,
                            'status code': status.HTTP_401_UNAUTHORIZED,
                            'message': 'Your account has not been verified. Please check your email for verification instructions.',
                        }
                        status_code = status.HTTP_401_UNAUTHORIZED
                        return Response(response, status_code)
                else:
                    response = {
                        'success': False,
                        'status code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Email or password is invalid. Please correct it and try again',
                    }
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(response, status_code)
        else:
            response = {
                'success': False,
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': "This account doesn't exist. Please go to signup or enter valid details",
            }
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status_code)
        

        

class SignOutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            
            Account.is_online = True
            Account.save()
            
            token.blacklist()
            response = {
                'success': 'True',
                'message': "Your account has been logged out successfully",
                'status code': status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': 'False',
                'message': "There is some problem while logging you out.",
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

class UserInterestView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInterestSerializer

    def get_queryset(self):
        return UserInterest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateInterestView(generics.RetrieveUpdateAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UpdateInterestSerializer
    permission_classes = [IsAuthenticated]
    
    # Modify the method to handle both GET and PATCH requests
    def get(self, request, *args, **kwargs):
        # Handle GET request to retrieve the interest
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Handle PATCH request to update the interest
        return self.partial_update(request, *args, **kwargs)
    



class FriendRequestListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def create(self, request, *args, **kwargs):
        # Ensure that the request is not duplicated
        from_user = request.user
        to_user_id = request.data.get('to_user')
        if FriendRequest.objects.filter(from_user=from_user, to_user_id=to_user_id).exists():
            return Response("Friend request already sent.", status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

class FriendRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    @action(detail=True, methods=['post'])
    def accept_request(self, request, pk=None):
        friend_request = self.get_object()
        if friend_request.to_user != request.user:
            return Response("You can only accept friend requests sent to you.", status=status.HTTP_400_BAD_REQUEST)

        friend_request.accepted = True
        friend_request.save()

        # Add users to each other's friend lists
        friend_request.from_user.user_friends.add(friend_request.to_user)
        friend_request.to_user.user_friends.add(friend_request.from_user)

        # Delete the friend request
        friend_request.delete()

        return Response("Friend request accepted and deleted successfully.", status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject_request(self, request, pk=None):
        friend_request = self.get_object()
        if friend_request.to_user != request.user:
            return Response("You can only reject friend requests sent to you.", status=status.HTTP_400_BAD_REQUEST)

        # Delete the friend request
        friend_request.delete()

        return Response("Friend request rejected and deleted successfully.", status=status.HTTP_200_OK)
    




class ListUserFriendsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get_queryset(self):
        user = self.request.user
        return user.user_friends.all()






class LoadUsersViewSet(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        json_file = request.data.get('json_file', None)

        if json_file is None:
            return Response({'error': 'JSON file is required in the request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = json.load(json_file)
        except json.JSONDecodeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        for user_info in data.get("users", []):
            # Set default values for fields
            email = user_info.get('name')+"@chat.com"
            username = user_info.get("name")
            age= user_info.get('age')

            # Create a new user instance
            user = Account(email=email, username=username)

# Set random age
            user.age = randint(1, 100)
            interests = user_info.get("interests", {})

            # Set is_verified and is_online to True
            user.is_verified = True
            user.is_online = True

            # Save the user to the database
            user.save()

            # Now that the user is saved, create and save user interests
            user_interests = []
            for interest, preference_score in interests.items():
                user_interest = UserInterest(user=user, interest=interest, preference_score=preference_score)
                user_interest.save()  # Save each user interest individually
                user_interests.append(user_interest)


        return Response({'message': 'Users loaded successfully'}, status=status.HTTP_201_CREATED)




class FriendRecommendationsView(APIView):
    # authentication_classes = [YourAuthenticationClass]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = self.request.user
        user_interests = current_user.user_interests.all()
        similar_users = Account.objects.filter(
            user_interests__in=user_interests
        ).exclude(id=current_user.id)

        similar_users_with_common_interests = []
        for user in similar_users:
            common_interests_count = user.user_interests.filter(
                interest__in=user_interests.values_list('interest', flat=True)
            ).count()
            similar_users_with_common_interests.append({'user': user, 'common_interests': common_interests_count})

        # Sort the similar users by the number of common interests in descending order
        similar_users_with_common_interests.sort(key=lambda x: x['common_interests'], reverse=True)

        # Get the recommended friends with common interests
        recommended_friends = [user_data['user'] for user_data in similar_users_with_common_interests]

        # If there are fewer than 5 recommended friends, add random users
        if len(recommended_friends) < 5:
            remaining_users = list(Account.objects.exclude(id=current_user.id))
            random_users = random.sample(remaining_users, 5 - len(recommended_friends))
            recommended_friends.extend(random_users)

        # Serialize the recommended friends
        serializer = AccountSerializer(recommended_friends, many=True)

        return Response({'recommended_friends': serializer.data}, status=status.HTTP_200_OK)
