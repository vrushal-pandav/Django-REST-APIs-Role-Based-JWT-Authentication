from django.urls import path
from .import views

from rest_framework_simplejwt.views import ( # type: ignore
    TokenObtainPairView, 
    TokenRefreshView, 
    TokenVerifyView, 
    TokenBlacklistView
)

urlpatterns = [
    
    # Sends an OTP to user's email for login or verification purposes.
    # Expects an email address in the request body.
    path('auth/email-otp/', views.SendOTPView.as_view()),

    # Logs in the user using the OTP sent to email.
    # Expects email and OTP in the request body. If valid, returns JWT tokens.
    path('auth/email-otp-login/', views.LoginWithOTPView.as_view()),
    
    # Blacklists the refresh token to log out the user.
    # Once blacklisted, the token cannot be used to refresh or access resources.
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Refreshes the access token using a valid refresh token.
    # Used when access token expires. Keeps the user logged in without re-authenticating.
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Verifies whether a given access or refresh token is still valid.
    # Good for debugging or confirming a token's status.
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]