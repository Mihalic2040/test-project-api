from ctypes import resize
from dataclasses import fields
import email
from unittest.util import _MAX_LENGTH, _MIN_END_LEN
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
# Create your models here.

class RegistrationSerializer(serializers.ModelSerializer):
    
    #email = serializers.EmailField(_MAX_LENGTH=50, _MIN_END_LEN=6)
    
    
    class Meta:
        model = User
        fields = ('username', "password", "email")

    def validate(self, args):
        username = args.get('nickname', None)
        password = args.get("password", None)
        email = args.get("email", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email alredy exists"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username" : "Username alredy exists"})
        
        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)