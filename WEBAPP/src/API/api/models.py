from dataclasses import fields
import email
from unittest.util import _MAX_LENGTH, _MIN_END_LEN
from django.db import models
from rest_framework import serializers
# Create your models here.

class RegistrationSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(_MAX_LENGTH=50, _MIN_END_LEN=6)
    
    
    class Meta:
        model = User
        fields = ('nickname', "password", "email")

    def validate(self, args):
        nickname = args.get('nickname' None)
        password = args.get("password" None)
        email = args.get("email", None)