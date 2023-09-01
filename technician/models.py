
from django.db import models
from accounts.models import CustomUser
from cloudinary.models import CloudinaryField
class TechnicianProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    profession = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    image = CloudinaryField('image',overwrite=True,format="jpg",null=True)
    description = models.TextField()

    def __str__(self):
        return self.user.username
    
