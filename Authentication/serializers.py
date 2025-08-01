from rest_framework import serializers
from .models import Roles, Users

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    role_id = RoleSerializer(read_only=True)
    
    class Meta:
        model = Users
        fields = ['id','email', 'contact_no', 'role_id']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class OTPLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=4, max_length=4)