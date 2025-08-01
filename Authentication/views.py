from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError # type: ignore
from.models import Users, OTPs
from.serializers import LoginSerializer, OTPLoginSerializer, UserSerializer

from .utils import validate_user_email, get_or_create_role_obj_by_name
from .utils import verify_otp
from django.db import transaction, IntegrityError

import random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings       
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_datetime

class SendOTPView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].strip().lower()
            validate_user_email(email) # utils.py function that Validate user email
                
            otp = str(random.randint(1000,9999))
            expired_at = timezone.now() + timedelta(minutes=5) # set OTP expiry time to 5 minutes
            otp_obj = OTPs.objects.create(
                email=email, 
                otp=otp,
                expired_at=expired_at,
                ) # Create OTP object
            
            try:
                send_mail(
                    subject="Your OTP Code",
                    message=f"Your OTP is {otp}",
                    from_email=settings.DEFAULT_FROM_EMAIL,  # or your email string like 'no-reply@yourdomain.com'
                    recipient_list=[email],  # must be a list of recipient emails
                    fail_silently=False,
                )
            except Exception as e:
                return JsonResponse({
                    "error": "error occurred while sending the email.",
                    "details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({'message': 'OTP sent to email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginWithOTPView(APIView):
    def post(self,request):                
        serializer = OTPLoginSerializer(data = request.data)
        created = False
        if serializer.is_valid():
            email = serializer.validated_data['email'].strip().lower()
            otp = serializer.validated_data['otp'].strip()
            
            if email == '':
                return Response({
                    "error":"Empty Email is not allowed"
                }, status=status.HTTP_400_BAD_REQUEST)
            if otp == '':
                return Response({
                    "error":"Empty OTP is not allowed"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # verify the otp
            otp_obj = verify_otp(email, otp)
            if isinstance(otp_obj, Response):  # OTP failed
                return otp_obj
            try:
                with transaction.atomic():
                    # Delete OTP
                    otp_obj.delete()
            
                    # Check if role exists or not if not exists then create role...
                    customer_role = get_or_create_role_obj_by_name('User')
                    try:
                        customer_obj = Users.objects.get(email=email,role_id=customer_role)
                        
                    except Users.DoesNotExist:
                        # Create user object role:User,
                        customer_obj = Users.objects.create(
                            email=email,
                            role_id=customer_role,
                        )
                        created=True
                
                # Generate JWT
                refresh = RefreshToken.for_user(customer_obj)
                user_serializer = UserSerializer(customer_obj, many=False,read_only=True)
                        
                # Success response
                return Response({
                    'message': 'Account Created Successfull' if created else 'Login Successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': user_serializer.data
                }, status=status.HTTP_200_OK)
            
            # Exception is occured when data base constraint is violated.
            except IntegrityError as e:
                return Response({
                    "error": "A database integrity error occurred. Please contact support."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            # Untracked exception 
            except Exception as e:
                return Response({
                    "error": "Something went wrong during login",
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)