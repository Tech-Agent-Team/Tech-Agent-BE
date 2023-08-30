from rest_framework import serializers
from .models import CustomUser
from technician.models import TechnicianProfile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'location', 'password', 'is_customer']
        
class CustomUserWithNoPassword(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'location', 'is_customer']
        
        
########################################################################
class CustomUserUpdateProfileCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'location']

# class TechnicianProfileupdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TechnicianProfile
#         fields = ['profession', 'image', 'description']
        
    
# class CustomUserUpdateProfileTechnicianSerializer(serializers.ModelSerializer):
#     # technicianprofile = TechnicianProfileupdateSerializer()  # Remove this line

#     class Meta:
#         model = CustomUser
#         fields = ['email', 'phone', 'location', 'technicianprofile']

#     def update(self, instance, validated_data):
#         technician_profile_data = validated_data.pop('technicianprofile', {})
#         instance = super().update(instance, validated_data)
        
#         technician_profile = instance.technicianprofile
#         for key, value in technician_profile_data.items():
#             setattr(technician_profile, key, value)
#         technician_profile.save()
        
#         return instance




