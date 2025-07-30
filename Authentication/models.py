from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class Roles(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
    
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, role_id=None, password=None, user_name=None,**extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)

        # Resolve roleID
        if role_id is None:
            role_obj,_ = Roles.objects.get_or_create(name='Customer')  # default role
        elif isinstance(role_id, int):
            role_obj = Roles.objects.get(pk=role_id)
        elif isinstance(role_id, str):
            role_obj,_ = Roles.objects.get_or_create(name=role_id)
        elif isinstance(role_id, Roles):
            role_obj = role_id
        else:
            raise ValueError("Invalid role_id")

        user = self.model(email=email, role_id=role_obj, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password, **extra_fields):
        user_name = email
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Remove roleID and accountSateID from extra_fields if present to avoid duplicate
        extra_fields.pop('role_id', None)
        extra_fields.pop('account_state_id', None)

        return self.create_user(email=email, password=password, role_id='Admin', account_state_id='Active',user_name=user_name, **extra_fields)
    

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField()
    user_name = models.CharField(max_length=50,unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
     
class OTPs(models.Model):
    email = models.EmailField()
    contact_no = models.CharField(max_length=15, null=True, blank=True)
    otp = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expired_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.email}, OTP: {self.otp}"