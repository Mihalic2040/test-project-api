"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from api.views import RegisterApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .yasg import urlpatterns as swagger_path
from api.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api-auth/', include('rest_framework.urls')),
    #path('', views.home),
    path('api/v1.0/aunt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1.0/aunt/token/verify/', TokenVerifyView.as_view(), name= "token_verify"),
    path('api/v1.0/aunt/register/', RegisterApi.as_view(), name="register"),
    path('api/v1.0/aunt/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1.0/aunt/email-activator/', EmailActivation.as_view(), name ="email-activator"),
    path('api/v1.0/aunt/reset-password/code', PasswordReseterCode.as_view(), name ="reset-password-get-code"),
    path('api/v1.0/aunt/reset-password/reset', PasswordReseter.as_view(), name ="reset-password"),
    path('api/v1.0/post/all', GetPost.as_view(), name ="Get all posts"),
    path('api/v1.0/post/create', CreatePost.as_view(), name ="Create Own posts"),
    path('api/v1.0/post/id', GetPostById.as_view(), name="Get_post_by_id"),
    path('api/v1.0/post/update', UpdatePost.as_view(), name="Update_post_by_id"),
    path('api/v1.0/post/setlike', SetLike.as_view(), name="Set_Like_by_id"),
    path('api/v1.0/post/getlike', GetLikes.as_view(), name="Get_Likes_by_post"),
    path('api/v1.0/post/search', SearchPost.as_view(), name="Search_post_by_title"),
    path('api/v1.0/profile/id', GetProfileById.as_view(), name="Get_profile_by_id"),
    path('api/v1.0/profile/update', UpdateProfile.as_view(), name="Update_profile_username"),
] + swagger_path

