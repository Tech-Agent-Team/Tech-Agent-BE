# # technicians/models.py
# from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from accounts.models import CustomUser

# class TechnicianProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
#     profession = models.CharField(max_length=255)
#     rating = models.IntegerField()
#     feedback = models.TextField()
#     image = models.CharField(max_length=255)
#     description = models.TextField()

# @receiver(post_save, sender=CustomUser)
# def create_technician_profile(sender, instance, created, **kwargs):
#     if created and instance.user_type == 'technician':
#         TechnicianProfile.objects.create(user=instance)
# technicians/models.py

from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from accounts.models import CustomUser

class TechnicianProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    profession = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    feedback = models.TextField()
    image = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.user.email
    
