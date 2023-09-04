
from .serializers import CustomerProfileSignUpSerializer, CustomerProfileSerializer, CustomermyordersSerializers, CustomerordersfeedSerializers
from accounts.serializers import CustomUserSerializer
from rest_framework.generics import ListAPIView
from accounts.permissions import IsCustomerUser
from orders.models import Order
from .models import CustomerProfile
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.http import Http404
from django.conf import settings
from django.core.mail import send_mail


class CustomerSignUpView(generics.GenericAPIView):
    serializer_class = CustomerProfileSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_data = request.data
        subject = 'Account created successfully'
        message = f'Dear {user_data["username"]},\n\nWe would like to inform your Customer Account has been successfully created!.\n\nIf you have any questions or need further assistance, please don\'t hesitate to contact us at ahmasamer51@gmail.com.\n\nThank you for choosing our services.\n\nSincerely,\nThe Tech Agent Team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_data["email"]]
        send_mail(subject, message, from_email,recipient_list, fail_silently=False)

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
            return Response(status=404)

        if order.owner != request.user.customerprofile:
            # Forbidden
            return Response({"detail": "Forbidden."}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        subject = 'Order Deleted Successfully'
        message = f'Dear Customer,\n\nWe would like to inform you that your order with ID {order_id}\n\n Order Description:\n\n {order.description}\n\n  has been deleted successfully.\n\nIf you have any feedback or would like to provide us with any details to help improve our services, please feel free to contact us at ahmasamer51@gmail.com.\n\nThank you for choosing our services.\n\nSincerely,\nThe Tech Agent Team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [order.owner.user.email]
        send_mail(subject, message, from_email,recipient_list, fail_silently=False)
        if order.current_technician :       
            subject = 'Order Was Cancelled'
            message = f'Dear Technician,\n\nWe would like to inform you that order you accepted with ID {order_id}\n\n Order Description:\n\n {order.description}\n\n  has been deleted by the customer.\n\nIf you have any feedback or would like to provide us with any details to help improve our services, please feel free to contact us at ahmasamer51@gmail.com.\n\nThank you for choosing our services.\n\nSincerely,\nThe Tech Agent Team'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [order.current_technician.user.email]
            send_mail(subject, message, from_email,recipient_list, fail_silently=False)

        order.delete()
        # Deletion successful
        return Response({"detail": "# Deletion successful."}, status=status.HTTP_204_NO_CONTENT)


class Customerordersdone(ListAPIView):
    permission_classes = [permissions.IsAuthenticated & IsCustomerUser]

    def put(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(status=404)  # Order not found

        # Check if the current user is the owner of the order
        if order.owner != request.user.customerprofile:
            # Forbidden
            return Response({"detail": "Forbidden."}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        if order.state_is_ongoing == False:
            return Response({"detail": "Order is not accepted yet by technician **state_is_ongoing"}, status=status.HTTP_400_BAD_REQUEST)
        if order.state_show == True:
            return Response({"detail": "Order is not accepted yet by technician **state_show"}, status=status.HTTP_400_BAD_REQUEST)

        order.state_is_ongoing = False
        order.state_show = False

        order.save()

        subject = 'Service is Complete'
        message = f'Dear Technician,\n\nWe are pleased to inform you that your order with ID {order_id}\n\n Order Description:\n\n {order.description}\n\n  has been successfully completed and rated by the customer.\n\nIf you have any further questions or need assistance, please feel free to contact us at ahmasamer51@gmail.com.\n\nThank you for choosing our services.\n\nSincerely,\nThe Tech Agent Team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [order.current_technician.user.email]
        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)

        message = f'Dear Customer,\n\nWe are pleased to inform you that your order with ID {order_id}\n\n Order Description:\n\n {order.description}\n\n  has been successfully completed and marked as complete.\n\nIf you have any further questions or need assistance, please feel free to contact us at ahmasamer51@gmail.com.\n\nThank you for choosing our services.\n\nSincerely,\nThe Tech Agent Team'
        recipient_list = [order.owner.user.email]
        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)

        # Deletion successful
        return Response({"detail": "#the order is done "}, status=status.HTTP_204_NO_CONTENT)


class Customerordersfeed(ListAPIView):
    permission_classes = [permissions.IsAuthenticated & IsCustomerUser]

    def put(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(status=404)  # Order not found

        # Check if the current user is the owner of the order
        if order.owner != request.user.customerprofile:
            # Forbidden
            return Response({"detail": "Forbidden."}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        if order.state_is_ongoing == True:
            return Response({"detail": "Order is state_is_ongoing"}, status=status.HTTP_400_BAD_REQUEST)
        if order.state_show == True:
            return Response({"detail": "Order is not accepted yet by technician **state_show"}, status=status.HTTP_400_BAD_REQUEST)
        # order.state_is_ongoing=False
        # order.state_show=False
        serializer = CustomerordersfeedSerializers(
            data=request.data, partial=True)
        if serializer.is_valid():
            feedback = serializer.validated_data.get('feedback')
            if feedback:
                order.feedback = feedback

            rating = serializer.validated_data.get('rating')
            if rating:
                order.rating = rating
            order.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerProfileSerializer

    def get_object(self):
        user_name = self.kwargs['user_name']
        try:
            customer_profile = CustomerProfile.objects.get(user__username=user_name)
            num_orders = Order.objects.filter(
                owner=customer_profile).values_list('created_at', flat=True)
            customer_profile.num_orders = len(num_orders)
            return customer_profile
        except CustomerProfile.DoesNotExist:
            raise Http404("Customer profile does not exist")
