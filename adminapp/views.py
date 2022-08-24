from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import transaction
from adminapp.serializers import UserSerializer
from myapp.authentication.authentication import cTokenAuthentication
from rest_framework.permissions import DjangoModelPermissions
from django.utils import timezone
# Create your views here.

class adminLogin(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            with transaction.atomic():
                userData = User.objects.get(
                    username =   data["username"],
                )
                if userData.is_superuser == 0:
                    return Response({"message":"Only admin can login", "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

                if userData.check_password(data["password"]):
                    if Token.objects.filter(user=userData).exists():
                        Token.objects.get(user=userData).delete()

                    userData.last_login = timezone.now()
                    userData.save()
                    token=Token.objects.create(user=userData)
               
                return Response({"username":data['username'], "message": "Login Successfully.Please use token for further process",
                                "token":token.key,
                                    "status": True, "response": "success", }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [cTokenAuthentication]
    permission_classes = [DjangoModelPermissions]
    queryset = User.objects.all()
    serializer_class=UserSerializer
    http_method_names = ['post','get','put']

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            with transaction.atomic():
                

                userData = User.objects.create(
                    username =   data["username"],
                    email = data["email"],
                    first_name =  data["first_name"],
                    last_name =  data["last_name"],
                    is_active = True,
                )
                
                userData.set_password(data["password"])
                userData.save()
               
                return Response({"username":data['username'], "message": "Your registration has been successfully completed.",
                                    "status": True, "response": "success", }, status=status.HTTP_200_OK)
        except Exception as error:
             return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        try:
            with transaction.atomic():
                userData = User.objects.filter(id=int(self.kwargs['pk'])).update(
                    email = data["email"],
                    first_name =  data["first_name"],
                    last_name =  data["last_name"],
                )

                user=User.objects.get(id=int(self.kwargs['pk']))
                                
                user.set_password(data["password"])
                user.save()
               
                return Response({"message": "User updated successfully",
                                    "status": True, "response": "success", }, status=status.HTTP_200_OK)
        except Exception as error:
             return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                userData = User.objects.all()

                data=self.serializer_class(userData,many=True).data
                return Response({"data":data,"message": "list",
                                    "status": True, "response": "success", }, status=status.HTTP_200_OK)
        except Exception as error:
             return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)