from django.http import request
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import CustomUserSerializer,CustomUserUpdateProfileSerializer
from .permissions import IsCustomerUser, IsTechnicianUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime, timedelta


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["email"] = user.email
        token["username"] = user.username
        token['is_customer']=user.is_customer
        token['is_technician']=user.is_technician
        
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsCustomerUser]
    serializer_class=CustomUserSerializer

    def get_object(self):
        return self.request.user

class TechnicianOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsTechnicianUser]
    serializer_class=CustomUserSerializer

    def get_object(self):
        return self.request.user



class CustomUserUpdateProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserUpdateProfileSerializer

    def get_object(self):
        return self.request.user  # Return the authenticated user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = CustomUserUpdateProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)