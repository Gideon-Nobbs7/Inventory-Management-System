from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
# Create your models here.


class ProfileManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field must be set")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.setdefault("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.setdefault("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self.create_user(username, password, **extra_fields)
    

class Profile(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = ProfileManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Profile with username {self.username}"