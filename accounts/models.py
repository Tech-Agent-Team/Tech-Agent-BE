
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=255,null=True, blank=True)
    location = models.CharField(max_length=255,null=True, blank=True)
    is_customer = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
