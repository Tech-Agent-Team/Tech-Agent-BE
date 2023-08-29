from rest_framework import generics ,permissions
from rest_framework.response import Response
from .serializers import TechnicianProfileSignUpSerializer,homeTechnicianSerializers
from accounts.serializers import CustomUserSerializer
from orders.models import Order
from rest_framework.generics import ListAPIView, RetrieveAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView
from accounts.permissions import IsTechnicianUser
# from rest_framework.authtoken.models import Token
# Create your views here.

class TechnicianSignUpView(generics.GenericAPIView):
    serializer_class = TechnicianProfileSignUpSerializer
    def post(self,request,*args, **kwargs):
        serializer= self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": CustomUserSerializer(user, context = self.get_serializer_context()).data,
                "message":"account created successfully"
            }
        )
    
class homeTechnicianView(ListAPIView):
    permission_classes=[permissions.IsAuthenticated&IsTechnicianUser]
    queryset= Order.objects.all()
    serializer_class=homeTechnicianSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)