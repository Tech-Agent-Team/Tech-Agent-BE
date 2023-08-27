from rest_framework import generics
from rest_framework.response import Response
from .serializers import CustomerProfileSignUpSerializer
from accounts.serializers import CustomUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class CustomerSignUpView(generics.GenericAPIView):
    serializer_class = CustomerProfileSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
                "token": Token.objects.get(user=user).key,
                "message": "account created successfully",
            }
        )
        
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'is_customer':user.is_customer
        })