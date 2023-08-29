from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer ,TechnicianProfileSerializer,CommentSerializer
from .models import Order,Comment
from rest_framework.generics import ListAPIView, RetrieveAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user.customerprofile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
class OrderAcceptanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id, *args, **kwargs):
        technician = request.user.technicianprofile

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if not order.state_show:
            return Response({"detail": "Order has already been accepted."}, status=status.HTTP_400_BAD_REQUEST)
        
        order.state_show = False
        order.state_is_ongoing = True

        # Validate the serializer before accessing the data
        serializer = TechnicianProfileSerializer(data=request.data)
        if serializer.is_valid():
            eta_arrival_time = serializer.validated_data.get('eta_arrival_time')
            if eta_arrival_time:
                order.eta_arrival_time = eta_arrival_time
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the current_technician field
        order.current_technician = technician
        
        order.save()
        
        return Response({"detail": "Order accepted successfully."}, status=status.HTTP_200_OK)
    


class UpdateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.owner != request.user.customerprofile:
            return Response({"detail": "You do not have permission to update this order."}, status=status.HTTP_403_FORBIDDEN)

        if order.state_is_ongoing:
            return Response({"detail": "Order is already ongoing and cannot be updated."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # This will perform a partial update of the existing order
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        sender = "customer" if request.user.is_customer else  "technician"
        # Check if the user is either the owner/customer or the current technician
        if sender== "customer":
            if order.owner == request.user.customerprofile :
                serializer = CommentSerializer(data=request.data , partial=True )
                if serializer.is_valid():
                    serializer.save(post=order, name=request.user.username ,sender=sender)  # Set the name to the username of the commenter
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "You are not authorized to comment on this order."}, status=status.HTTP_403_FORBIDDEN)
        if sender== "technician":
            if (order.current_technician and order.current_technician.user == request.user):
                serializer = CommentSerializer(data=request.data , partial=True )
                if serializer.is_valid():
                    serializer.save(post=order, name=request.user.username ,sender=sender)  # Set the name to the username of the commenter
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "You are not authorized to comment on this order."}, status=status.HTTP_403_FORBIDDEN)


class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is either the owner/customer or the current technician
        if order.owner == request.user.customerprofile or (order.current_technician and order.current_technician.user == request.user):
            comments = Comment.objects.filter(post=order)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You are not authorized to access this order's comments."}, status=status.HTTP_403_FORBIDDEN)









# class CommentDetailView(APIView):
#     def get(self, request, comment_id, *args, **kwargs):
#         try:
#             comment = Comment.objects.get(id=comment_id)
#         except Comment.DoesNotExist:
#             return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = CommentSerializer(comment)
#         return Response(serializer.data, status=status.HTTP_200_OK)