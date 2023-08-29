
from django.db import models
from accounts.models import CustomUser

class TechnicianProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    profession = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    feedback = models.TextField()
    image = models.ImageField(upload_to='uploads/', blank=True,null=True)
    description = models.TextField()

    def __str__(self):
        return self.user.username
    
