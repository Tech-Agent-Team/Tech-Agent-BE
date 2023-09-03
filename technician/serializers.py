from rest_framework import serializers
from .models import TechnicianProfile , Profession

from orders.models import Order ,Comment
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from accounts.serializers import CustomUserSerializer,CustomUserWithNoPassword

class TechnicianProfileSignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    professions = serializers.ListField(child=serializers.CharField(max_length=255))
    image = serializers.CharField(max_length=255)
    description = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'image', 'description', 'professions']
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

        technician_profile = TechnicianProfile.objects.create(
            user=user,
            image=self.validated_data['image'],
            description=self.validated_data['description']
        )

        professions = self.validated_data.get('professions', [])
        for profession in professions:
            Profession.objects.create(
                technicianProfession=technician_profile,
                techProfession=profession
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
          
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class TechnicianAcceptedOrdersSerializers(serializers.ModelSerializer):
    customer_name = CustomUserSerializerInfo(source='owner.user', read_only=True)
    comments = CommentSerializer(many=True, read_only=True, default=[{'text': 'Default Comment'}])

    class Meta:
        model = Order
        fields = ['id', 'description', 'image', 'technician_type', 'eta_arrival_time', 'customer_name', 'comments']



class TechnicianProfileSerializer(serializers.ModelSerializer):
    user = CustomUserWithNoPassword()
    average_rating = serializers.FloatField()
    feedback_list = serializers.ListField()
    professions = serializers.StringRelatedField(many=True)  # Assuming 'professions' is a related field in TechnicianProfile

    class Meta:
        model = TechnicianProfile
        fields = ['user', 'professions', 'image', 'description', 'average_rating', 'feedback_list']


class TechnicianUpdateProfileSerializer(serializers.ModelSerializer):
    professions = serializers.ListField(child=serializers.CharField(max_length=255), required=False)

    class Meta:
        model = TechnicianProfile
        fields = ['professions', 'image', 'description']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['professions'] = [profession.techProfession for profession in instance.professions.all()]
        return data

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        
        professions = validated_data.get('professions', [])
        if professions is not None:
            instance.professions.all().delete()
            for profession in professions:
                Profession.objects.create(technicianProfession=instance, techProfession=profession)
        
        instance.save()
        return instance