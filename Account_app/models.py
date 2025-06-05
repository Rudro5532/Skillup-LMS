from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100, blank=True)


    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','username']

    def __str__(self):
        return self.full_name


    