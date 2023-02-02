from asyncio import tasks

from . import tasks
from rest_framework import generics
from api.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Utils
from django.contrib.sites.shortcuts import  get_current_site
from django.urls import reverse


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
            
            User_data = serializer.data

            user = User.objects.get(email=User_data['email'])

            data = {
                "to_email": user.email,
                "email_subject": "Verify your email",
            }
                
            Utils.activate_mail(data=data)

            return Response({
                "msg": "Check email to verify account!"
            },status=status.HTTP_201_CREATED)



        return Response({
            "error": "User not created"
        },status=status.HTTP_400_BAD_REQUEST)



class EmailActivation(generics.GenericAPIView):

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
        
        return Response({
            "msg": 'Something went wrong'
        },status=status.HTTP_400_BAD_REQUEST)
    

class PasswordReseterCode(generics.GenericAPIView):

    serializer_class = ChangePasswordSerializer

    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)

        if (serializer.is_valid()):
            
            User_data = serializer.data
            email = User_data['email']

            user = User.objects.filter(email= email)
            user_mail = User.objects.get(email=User_data['email'])
            if not user.exists():
                return Response({
                    'msg': 'This User not exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            data = {
                "to_email": user_mail.email,
                "email_subject": "Password reset code!",
            }

            Utils.reset_pass(data=data)

            return Response({
                'msg': 'Check email to see a restore code.'
            },status=status.HTTP_200_OK)


        return Response({
            'msg': 'Someting went wrong'
        },status=status.HTTP_400_BAD_REQUEST)
        


class PasswordReseter(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializerPUT

    def put(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)

        if (serializer.is_valid()):
            User_data = serializer.data
            email = User_data['email']
            otp = User_data['otp']
            new_password = User_data['new_password']


            
            user = User.objects.filter(email= email)

            if not user.exists():
                return Response({
                    'msg': 'This User not exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            if user[0].otp != otp:
                return Response({
                    'msg': "Invalid reset code"
                },status=status.HTTP_400_BAD_REQUEST)
            
            user = user.first()

            hash_password = make_password(new_password)

            user.password = str(hash_password)

            user.save()

            return Response({
                'msg': 'Passoword has been cahnged!'
            },status=status.HTTP_200_OK)

        return Response({
            'msg': 'Someting went wrong'
        },status=status.HTTP_400_BAD_REQUEST)

