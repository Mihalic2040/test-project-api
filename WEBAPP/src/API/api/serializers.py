
from rest_framework import serializers
from .models import User
from .models import Post
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


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    email = serializers.EmailField(required=True)
   



class ChangePasswordSerializerPUT(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class GetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','owner_id','title','content','post_date',)


class CreatePostSerializer(serializers.Serializer):

    model = Post
 

    title = serializers.CharField(required=True)

    content = serializers.CharField(required=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
class GetPostByIdSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ('id',)