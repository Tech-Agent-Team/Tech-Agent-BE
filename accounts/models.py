# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     email = models.CharField(max_length=255)
#     phone = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     USER_TYPE_CHOICES = (
#         ('customer', 'Customer'),
#         ('technician', 'Technician'),
#     )
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    is_customer = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
# @receiver(post_save,sender = settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user = instance)