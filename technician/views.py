from rest_framework import generics ,permissions
from rest_framework.response import Response
from .serializers import TechnicianProfileSignUpSerializer,homeTechnicianSerializers
from accounts.serializers import CustomUserSerializer
from orders.models import Order
from rest_framework.generics import ListAPIView, RetrieveAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView,DestroyAPIView
from accounts.permissions import IsTechnicianUser
from .models import TechnicianProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from orders.serializers import OrderSerializer
from rest_framework.views import APIView

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

class TechnicianAcceptedOrdersView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Use only IsAuthenticated permission

    serializer_class = homeTechnicianSerializers
    
    def get_queryset(self):
        current_user = self.request.user  # Assuming the identifier is the username
        try:
            technician = TechnicianProfile.objects.get(user=current_user)
            
            queryset = Order.objects.filter(current_technician=technician, state_is_ongoing=True)
            return queryset
    
        except TechnicianProfile.DoesNotExist:
            return Order.objects.none()
            
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class TechnicianCancelOrdersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if order.current_technician != request.user.technicianprofile:
            return Response({"detail": "You do not have permission to update this order."}, status=status.HTTP_403_FORBIDDEN)


        order.current_technician = None
        order.eta_arrival_time = None
        order.state_is_ongoing = False
        order.state_show = True
        order.save()

        return Response({"detail": "Order cancelled successfully."}, status=status.HTTP_200_OK)
