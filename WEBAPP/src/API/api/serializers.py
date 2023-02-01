
from rest_framework import serializers
from .models import User

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

class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


