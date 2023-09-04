from django.db import models
from accounts.models import CustomUser
from cloudinary.models import CloudinaryField

class TechnicianProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    image = CloudinaryField('image',overwrite=True,format="jpg",null=True)
    description = models.TextField()

    def __str__(self):
      return   self.user.username 
class Profession(models.Model):

    technicianProfession=models.ForeignKey(TechnicianProfile,on_delete=models.CASCADE,related_name='professions')
    techProfession = models.TextField()

    def __str__(self):
            return f"{self.technicianProfession.user.username} :  is a ( {self.techProfession}) "
