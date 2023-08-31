
from rest_framework import serializers
from .models import CustomerProfile
from accounts.models import CustomUser
from orders.models import Order,Comment

class CustomerProfileSignUpSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type": "password"},write_only=True)
    class Meta:
        model= CustomUser
        fields = ['username','email', 'password', 'password2']
        extra_kwargs={
            'password': {'write_only': True}
        }
        
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
    

class CustomUserSerializerInfo(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Replace with your actual CustomUser model
        fields = ['username']  # Add the relevant fields
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
class CustomermyordersSerializers(serializers.ModelSerializer):
    technician_name = CustomUserSerializerInfo(source='current_technician.user', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class CustomerordersfeedSerializers(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields =('feedback','rating')

class CustomerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField(source='user.phone')
    location = serializers.CharField(source='user.location')
    is_customer = serializers.BooleanField(source='user.is_customer')
    num_orders = serializers.SerializerMethodField()

    class Meta:
        model = CustomerProfile
        fields = ['username', 'email', 'phone', 'location', 'is_customer', 'num_orders']
    
    def get_num_orders(self, instance):

        return instance.order_set.count()  # Adjust this to match your actual relationship name


    class CustomUserUpdateProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ['email', 'phone', 'location', 'password']