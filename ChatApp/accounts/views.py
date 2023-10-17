from accounts.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Account

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