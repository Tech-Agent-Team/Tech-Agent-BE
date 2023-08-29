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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
