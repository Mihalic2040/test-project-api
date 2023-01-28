from asyncio import tasks
from . import tasks
from rest_framework import generics
from api.models import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
# Create your views here.

def home(request):

    tasks.log_console.delay()

    return Response("Hello World")


class RegisterApi(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                "msg": "User created"
            },status=status.HTTP_201_CREATED)

        return Response({
            "error": "User not created"
        },status=status.HTTP_400_BAD_REQUEST)