# # customers/models.py
# from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from accounts.models import CustomUser

# class CustomerProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

# @receiver(post_save, sender=CustomUser)
# def create_customer_profile(sender, instance, created, **kwargs):
#     if created and instance.user_type == 'customer':
#         CustomerProfile.objects.create(user=instance)

# customers/models.py

from django.db import models
from accounts.models import CustomUser

class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
