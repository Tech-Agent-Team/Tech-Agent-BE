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
        



class CustomUserUpdateProfileCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'location']

    def update(self, instance, validated_data):
        email = validated_data.get('email', instance.email)

        # Check if the email already exists for other users
        if CustomUser.objects.exclude(pk=instance.pk).filter(email=email).exists():
            raise serializers.ValidationError("Email already exists for another user.")

        instance.email = email
        instance.phone = validated_data.get('phone', instance.phone)
        instance.location = validated_data.get('location', instance.location)
        instance.save()

        return instance


