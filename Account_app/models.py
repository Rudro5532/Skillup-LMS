from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import os

class User(AbstractUser):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to="profile_image/", blank=True)


    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','username']

    def __str__(self):
        return self.full_name
    
    def delete(self, *args, **kwargs):
        try:
            if self.profile_image and os.path.isfile(self.profile_image.path):
                os.remove(self.profile_image.path)
        except PermissionError:
            print(f"Permission denied while deleting: {self.profile_image.path}")
        except Exception as e:
            print(f"Unexpected error while deleting profile image: {e}")
        super().delete(*args, **kwargs)





class PasswordResetOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=5)



    