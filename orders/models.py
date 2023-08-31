# from django.db import models
# from customer.models import CustomerProfile
# from technician.models import TechnicianProfile
# # Create your models here.
# # technicians/models.py

# class Order(models.Model):
#     feedback = models.TextField()
#     rating = models.IntegerField()
#     state_is_ongoing = models.BooleanField(default=True)
#     state_show = models.BooleanField(default=True)
#     eta_arrival_time = models.DateTimeField()
#     description = models.TextField()
#     technician_type = models.CharField(max_length=255)
#     image = models.CharField(max_length=255)
#     adress = models.CharField(max_length=255)
    
#     owner = models.ForeignKey("app.Model", on_delete=models.DO_NOTHING)
#     current_technician = models.ForeignKey("app.Model", on_delete=models.DO_NOTHING)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)



from django.db import models
from customer.models import CustomerProfile
from technician.models import TechnicianProfile

class Order(models.Model):
    feedback = models.TextField()
    rating = models.IntegerField(default=10)
    state_is_ongoing = models.BooleanField(default=False)
    state_show = models.BooleanField(default=True)
    eta_arrival_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    technician_type = models.CharField(max_length=255)
    image =models.ImageField(upload_to='uploads/', blank=True,null=True)
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