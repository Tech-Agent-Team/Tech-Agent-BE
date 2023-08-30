from rest_framework import serializers
from .models import TechnicianProfile
from orders.models import Order
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from accounts.serializers import CustomUserSerializer,CustomUserWithNoPassword

class TechnicianProfileSignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    profession = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=255)
    description = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'profession', 'image', 'description']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate_email(self, value):
        user_model = get_user_model()
        if user_model.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already registered.")
        return value
    
    def save(self, **kwargs):
        user = CustomUser(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "password do not match"})
        user.set_password(password)
        user.is_technician = True
        user.save()

        TechnicianProfile.objects.create(
            user=user,
            profession=self.validated_data['profession'],
            image=self.validated_data['image'],
            description=self.validated_data['description']
        )
        return user
    
class homeTechnicianSerializers(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['id','description','image','technician_type','eta_arrival_time']
         
class CustomUserSerializerInfo(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Replace with your actual CustomUser model
        fields = ['username']  # Add the relevant fields
          
class TechnicianAcceptedOrdersSerializers(serializers.ModelSerializer):
    customer_name = CustomUserSerializerInfo(source='owner.user', read_only=True)  # Assuming 'owner' is the ForeignKey to CustomerProfile
    class Meta:
        model=Order
        fields=['id','description','image','technician_type','eta_arrival_time','customer_name']
   
class TechnicianProfileSerializer(serializers.ModelSerializer):
    user = CustomUserWithNoPassword()
    average_rating = serializers.FloatField()
    feedback_list = serializers.ListField()
    
    class Meta:
        model = TechnicianProfile
        fields = ['user', 'profession','image', 'description', 'average_rating','feedback_list']
