from rest_framework import serializers
from .models import Order

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
