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
from unicodedata import name
from django.contrib import admin
from django.urls import path
from api import views
from django.conf.urls import include
from api.views import RegisterApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .yasg import urlpatterns as swagger_path
from api.views import EmailActivation



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api-auth/', include('rest_framework.urls')),
    #path('', views.home),
    path('api/v1.0/aunt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1.0/aunt/token/verify/', TokenVerifyView.as_view(), name= "token_verify"),
    path('api/v1.0/auth/register/', RegisterApi.as_view(), name="register"),
    path('api/v1.0/aunt/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1.0/aunt/email-activator/', EmailActivation.as_view(), name ="email-activator"),   
] + swagger_path

