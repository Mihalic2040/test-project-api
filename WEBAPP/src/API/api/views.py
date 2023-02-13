from rest_framework import generics
from api.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import User
from .utils import Utils
from rest_framework import permissions
from fuzzywuzzy import process

# Create your views here.

class RegisterApi(generics.GenericAPIView):

     serializer_class = RegistrationSerializer

     permission_classes = [permissions.AllowAny,]

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

    permission_classes = [permissions.AllowAny,]

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

    permission_classes = [permissions.AllowAny,]

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

    permission_classes = [permissions.AllowAny,]

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



# get post using to get all post or one by id

class GetPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = GetPostSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):

        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = GetPostSerializer(queryset, many=True)
        return Response(serializer.data)

class CreatePost(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated,]

    serializer_class = CreatePostSerializer

    def post(self, request):

        data = request.data

        user = request.user
            
        owner_id = user.id
            

        serializer = self.get_serializer(data = data)
        

        if (serializer.is_valid()):
            serializer.save(owner_id=request.user.id)
            
            return Response({
                'msg': 'Post created'
            },status=status.HTTP_200_OK)

        return Response({
        'msg': 'Some thing went wrong'
        }, status=status.HTTP_400_BAD_REQUEST)


class GetPostById(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated,]

    serializer_class = GetPostByIdSerializer


    def post(self,request):
        data = request.data
        serializer = self.get_serializer(data=data)

        if (serializer.is_valid()):
            post = Post.objects.filter(id=data['id'])

            post_structure = {
                "id": post[0].id,
                "owner_id": post[0].owner_id,
                "title": post[0].title,
                "content": post[0].content,
                "post_date": post[0].post_date,
            }

            return Response(post_structure,status=status.HTTP_200_OK)
        

        return Response({
            'msg': 'Something went wrong or wrong id'
        },status=status.HTTP_400_BAD_REQUEST)
    

class UpdatePost(generics.UpdateAPIView):

    permission_classes = [permissions.IsAuthenticated,]

    serializer_class = UpdatePostSerializer

    def put(self,request):
        data = request.data

        serializer = self.get_serializer(data=data)

        if(serializer.is_valid()):
            main_post = Post.objects.filter(id=data['id'])

            if main_post[0].owner_id == request.user.id:

                post = main_post.first()

                post.title = data['title']

                post.content = data['content']

                post.save()

                return Response({
                    'msg': "Post updated"
                },status=status.HTTP_200_OK)

            return Response({
                    'msg': "You can update only own post"
                },status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'msg': 'Something went wrong or wrong id'
        },status=status.HTTP_400_BAD_REQUEST)
    

class GetProfileById(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]

    serializer_class = GetProfileSerializer

    def post(self, request):
        data = request.data

        serializer = self.get_serializer(data=data)

        if (serializer.is_valid()):
            user = User.objects.filter(id=data['id'])

            returned_data = {
                'id': user[0].id,
                'nickname': user[0].username
            }

            return Response(returned_data,status=status.HTTP_200_OK)

        return Response({
            'msg': 'Something went wrong or wrong id'
        },status=status.HTTP_400_BAD_REQUEST)
    

class UpdateProfile(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,]

    serializer_class = UpdateProfileSerializer

    def put(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)

        if (serializer.is_valid()):

            user = User.objects.filter(id=request.user.id)

            main_user = user.first()

            main_user.username = data['username']

            main_user.save()

            return Response({
                'msg': 'Profile Updated'
            },status=status.HTTP_200_OK)
        return Response({
            'msg': 'Something went wrong'
        },status=status.HTTP_400_BAD_REQUEST)
    


class SearchPost(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Post.objects.all()
    serializer_class = SearchPostSerializer

    def post(self, request):
        
        data = request.data
        serializer = self.get_serializer(data=data)

        if (serializer.is_valid()):
            queryset = self.get_queryset()
            q_serializer = GetPostSerializer(queryset, many=True)
            all_data = q_serializer.data


            title_list = []
            for item in all_data:
                title_list.append(item['title'])

            extraxted_data_raw = process.extract(data['title'], title_list)

            extraxted_data = extraxted_data_raw[0]
            extraxted_data = extraxted_data[0]

            post_obj = Post.objects.filter(title=extraxted_data)

            post =  {
                "id": post_obj[0].id,
                "owner_id": post_obj[0].owner_id,
                "title": post_obj[0].title,
                "content": post_obj[0].content,
                "post_date": post_obj[0].post_date,
            }

            return Response(post, status=status.HTTP_200_OK)

        return Response({
            'msg': 'Something went wrong'
        },status=status.HTTP_400_BAD_REQUEST)
    

class SetLike(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]

    serializer_class = SetLikeSerializer

    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)

        if (serializer.is_valid()):
            post_obj = Post.objects.get(id=data['post_id'])
            if request.user.id != post_obj.owner_id:
                if Like.objects.filter(owner=request.user.id, post_id=post_obj.id).exists():
                    Like.objects.filter(owner=request.user.id, post_id=post_obj.id).delete()
                    return Response({
                        'msg': 'Like Unset'
                    },status=status.HTTP_200_OK)
                else:
                    Like.objects.create(owner=request.user, post_id=post_obj)
                    return Response({
                        'msg': 'Like set'
                    },status=status.HTTP_200_OK)

            return Response({
                'msg': 'You can not like own post'
            },status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'msg': 'Something went wrong'
        },status=status.HTTP_400_BAD_REQUEST)
    

class GetLikes(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]

    serializer_class = GetLikesSerializer

    def post(self,request):
        data = request.data
        serializer = self.get_serializer(data=data)


        if (serializer.is_valid()):
            likes = Like.objects.filter(post_id=data['post_id'])
            

            like_list = likes

            final_data = []
            for item in likes:
                final_data.append(str(item.owner_id))


            return Response({
                'data': str(final_data)
            },status=status.HTTP_200_OK)
        

        return Response({
            'msg': 'Something went wrong'
        },status=status.HTTP_400_BAD_REQUEST)