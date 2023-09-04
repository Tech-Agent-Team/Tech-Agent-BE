from rest_framework import serializers
from .models import Order,Comment

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['description',  'technician_type', 'image', 'address','location']


class TechnicianProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('eta_arrival_time',)


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['description',  'technician_type', 'image', 'address','location']
        
        
# class UpdateOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['description', 'technician_type', 'image', 'address', 'location']

    def update(self, instance, validated_data):
        # Loop through the fields in the serializer's Meta class and update them
        for field in self.Meta.fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        # Save the instance to update the database
        instance.save()

        return instance

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
