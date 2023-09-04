from django.db import models
from customer.models import CustomerProfile
from technician.models import TechnicianProfile
from cloudinary.models import CloudinaryField
class Order(models.Model):
    feedback = models.TextField()
    rating = models.IntegerField(default=10)
    state_is_ongoing = models.BooleanField(default=False)
    state_show = models.BooleanField(default=True)
    eta_arrival_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    technician_type = models.CharField(max_length=255)
    image = CloudinaryField('image',overwrite=True,format="jpg",null=True)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    current_technician = models.ForeignKey(TechnicianProfile, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, null=True, blank=True, default='Some Default Location')
    
class Comment(models.Model):

    post=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    body = models.TextField()
    sender= models.CharField(max_length=255 ,null=True)

    def __str__(self):
        return self.name