from asyncio import tasks

from . import tasks
from rest_framework import generics
from api.serializers import RegistrationSerializer, ActivationSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Utils
from django.contrib.sites.shortcuts import  get_current_site
from django.urls import reverse


# Create your views here.

def home(request):

    tasks.log_console.delay()

    return Response("Hello World")


class RegisterView(generics.GenericAPIView):


    def post(self, request):
        user = request.data
        


class RegisterApi(generics.GenericAPIView):

     serializer_class = RegistrationSerializer

     def post(self, request):
        serializer = self.get_serializer(data = request.data)
         
        if(serializer.is_valid()):
            serializer.save()
            
            User_data = serializer.data

            user = User.objects.get(email=User_data['email'])

            token = RefreshToken.for_user(user).access_token

            current_site = get_current_site(request)

            relative_link = reverse("email-activator")
            
            absurl = "http://"+str(current_site)+relative_link+"?token= " + str(token)

            email_body = "To activate account click this link: \n" + absurl 

            data = {
                "to_email": user.email,
                "email_body": email_body,
                "email_subject": "Verify your email",
            }
                
            Utils.send_mail(data=data)

            return Response({
                "msg": "Check email to verify account!"
            },status=status.HTTP_201_CREATED)



        return Response({
            "error": "User not created"
        },status=status.HTTP_400_BAD_REQUEST)



class EmailActivation(generics.UpdateAPIView):

    serializer_class = ActivationSerializer

    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)

        if(serializer.is_valid()):
            
            User_data = serializer.data
            email = User_data['email']
            otp = User_data['otp']

            user = User.objects.filter(email= email)

            if not user.exists():
                return Response({
                    'msg': 'This User not exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            if user[0].otp != otp:
                return Response({
                    'msg': 'Invalid activation code'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = user.first()

            user.is_active = True

            user.save()


            return Response({
            'msg': 'Account is active now!'
            }, status=status.HTTP_200_OK)