
from django.db import models
from accounts.models import CustomUser

class TechnicianProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    profession = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    image = models.URLField(blank=True , default=None)
    description = models.TextField()

    def __str__(self):
        return self.user.username
    
