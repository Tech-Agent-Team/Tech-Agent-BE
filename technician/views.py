from rest_framework import generics ,permissions
from rest_framework.response import Response
from .serializers import TechnicianProfileSignUpSerializer,homeTechnicianSerializers,TechnicianProfileSerializer,TechnicianAcceptedOrdersSerializers
from accounts.serializers import CustomUserSerializer
from orders.models import Order
from rest_framework.generics import ListAPIView, RetrieveAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView,DestroyAPIView
from accounts.permissions import IsTechnicianUser
from .models import TechnicianProfile , Profession
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from .serializers import TechnicianUpdateProfileSerializer
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
    permission_classes = [permissions.IsAuthenticated & IsTechnicianUser]
    serializer_class = homeTechnicianSerializers

    def get_queryset(self):
        current_user = self.request.user
        try:
            technician = TechnicianProfile.objects.get(user=current_user)
            professions = Profession.objects.filter(technicianProfession=technician)
            profession_names = [profession.techProfession for profession in professions]
            
            # Filter orders by state_show=True and technician_type in profession_names
            queryset = Order.objects.filter(state_show=True, technician_type__in=profession_names)
            return queryset
        except TechnicianProfile.DoesNotExist:
            return Order.objects.none()
            
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class TechnicianAcceptedOrdersView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated & IsTechnicianUser]
    serializer_class = TechnicianAcceptedOrdersSerializers
    
    def get_queryset(self):
        current_user = self.request.user

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
    permission_classes = [IsAuthenticated  & IsTechnicianUser]
    
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

class TechnicianProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TechnicianProfileSerializer
    
    def get_object(self):
        try :
            user_name = self.kwargs['user_name']
            
            technician_profile = TechnicianProfile.objects.get(user__username=user_name)
            
            average_rating = Order.objects.filter(current_technician=technician_profile).values_list('rating', flat=True)
            feedback_list = Order.objects.filter(current_technician=technician_profile).values_list('feedback', flat=True)

            num = 0
            sum_rating = 0
            
            for rating in average_rating:
                if rating != None:
                    num += 1
                    sum_rating += float(rating)
            
            if num :
                avg_rating = sum_rating / num
            else:
                avg_rating = 10

            technician_profile.average_rating = round(avg_rating,1)
            
            print(technician_profile.average_rating)
            technician_profile.feedback_list = list(feedback_list)

            return technician_profile
        except TechnicianProfile.DoesNotExist:
            raise Http404("Technician does not Exist")

class TechnicianInfoUpdateProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated & IsTechnicianUser]
    serializer_class = TechnicianUpdateProfileSerializer

    def get_object(self):
        return self.request.user.technicianprofile

    def put(self, request, *args, **kwargs):
        technician_profile = self.get_object()

        serializer = TechnicianUpdateProfileSerializer(technician_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)