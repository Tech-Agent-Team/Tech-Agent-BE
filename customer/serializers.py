from rest_framework import serializers
from .models import CustomerProfile
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from orders.models import Order

class CustomerProfileSignUpSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type": "password"},write_only=True)
    class Meta:
        model= CustomUser
        fields = ['username','email', 'password', 'password2']
        extra_kwargs={
            'password': {'write_only': True}
        }
        
    def validate_email(self, value):
        user_model = get_user_model()
        if user_model.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already registered.")
        return value
    
    def save(self, **kwargs):
        user = CustomUser(
            username = self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error":"The passwords do not match"})
        user.set_password(password)
        user.is_customer = True

        user.save()
        CustomerProfile.objects.create(user = user)
        return user
    

class CustomermyordersSerializers(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = '__all__'


