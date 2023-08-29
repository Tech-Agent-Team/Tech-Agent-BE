from rest_framework import generics
from rest_framework.response import Response
from .serializers import CustomerProfileSignUpSerializer ,CustomermyordersSerializers 
from accounts.serializers import CustomUserSerializer
from rest_framework.generics import ListAPIView
from rest_framework import generics ,permissions
from accounts.permissions import IsCustomerUser
from orders.models import Order
from .models import CustomerProfile
from django.db.models import Q
from rest_framework import status





class CustomerSignUpView(generics.GenericAPIView):
    serializer_class = CustomerProfileSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
                # "token": Token.objects.get(user=user).key,
                "message": "account created successfully",
            }
        )
        


class Customermyorders(ListAPIView):
    permission_classes = [permissions.IsAuthenticated & IsCustomerUser]
    serializer_class = CustomermyordersSerializers

    def get_queryset(self):
        current_user = self.request.user
        try:
            customer_profile = CustomerProfile.objects.get(user=current_user)
            queryset = Order.objects.filter(
                Q(owner=customer_profile) &
                (Q(state_is_ongoing=True) | Q(state_show=True))
            )
            return queryset
        except CustomerProfile.DoesNotExist:
            return Order.objects.none()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    


class Customerdeletorders(ListAPIView):
    permission_classes = [permissions.IsAuthenticated & IsCustomerUser]

    def delete(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(status=404)  # Order not found

        # Check if the current user is the owner of the order
        if order.owner != request.user.customerprofile:
            return Response({"detail": "Forbidden."}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)  # Forbidden
        # if order.state_is_ongoing:
        #     return Response({"detail": "Order is already ongoing and cannot be delete."}, status=status.HTTP_400_BAD_REQUEST)
        order.delete()
        return Response({"detail": "# Deletion successful."}, status=status.HTTP_204_NO_CONTENT) # Deletion successful
    

class Customerordersdone(ListAPIView):
    permission_classes = [permissions.IsAuthenticated & IsCustomerUser]

    def put(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(status=404)  # Order not found

        # Check if the current user is the owner of the order
        if order.owner != request.user.customerprofile:
            return Response({"detail": "Forbidden."}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)  # Forbidden
        if order.state_is_ongoing==False:
            return Response({"detail": "Order is not accepted yet by technician **state_is_ongoing"}, status=status.HTTP_400_BAD_REQUEST)
        if order.state_show ==True:
            return Response({"detail": "Order is not accepted yet by technician **state_show"}, status=status.HTTP_400_BAD_REQUEST)
        order.state_is_ongoing=False
        order.state_show=False
        order.save()
        return Response({"detail": "#the order is done "}, status=status.HTTP_204_NO_CONTENT) # Deletion successful
    



