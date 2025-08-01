from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken # type: ignore
from rest_framework import status
from rest_framework.response import Response
from .models import Roles, OTPs

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.utils import timezone


def blacklist_user_tokens(user):
    for token in OutstandingToken.objects.filter(user=user):
        BlacklistedToken.objects.get_or_create(token=token)

def get_or_create_role_obj_by_name(role_name):
    role_obj, _ = Roles.objects.get_or_create(name=role_name)
    return role_obj


def validate_user_email(email):
    try:
        validate_email(email)
    except ValidationError:
        return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

def verify_otp(email,otp):
    try:
        otp_obj = OTPs.objects.filter(
            email=email,
            otp=otp,
            is_used=False,
        ).latest('timestamp')
    except OTPs.DoesNotExist:
        return Response({
            "error":"Invalid OTP"
        }, status=status.HTTP_400_BAD_REQUEST)
            
    if otp_obj.expired_at < timezone.now():
        return Response({
            "error":"OTP has expired. Please request a new OTP."
        }, status=status.HTTP_400_BAD_REQUEST)
    return otp_obj
    