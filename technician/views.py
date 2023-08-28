from rest_framework import generics
from rest_framework.response import Response
from .serializers import TechnicianProfileSignUpSerializer
from accounts.serializers import CustomUserSerializer
# from rest_framework.authtoken.models import Token
# Create your views here.

class CustomerSignUpView(generics.GenericAPIView):
    serializer_class = TechnicianProfileSignUpSerializer
    def post(self,request,*args, **kwargs):
        serializer= self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": CustomUserSerializer(user, context = self.get_serializer_context()).data,
                # "token": Token.objects.get(user = user).key,
                "message":"account created successfully"
            }
        )
    

