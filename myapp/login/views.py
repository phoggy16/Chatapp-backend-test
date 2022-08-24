from rest_framework import status,viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.db import transaction
from adminapp.serializers import UserSerializer
from django.utils import timezone
from myapp.authentication.authentication import cTokenAuthentication
from rest_framework.permissions import DjangoModelPermissions

class AuthLoginViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class=UserSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            data=request.data
            username=data['username']
            with transaction.atomic():
                if User.objects.filter(username=username).exists():
                    password = request.data['password']
                    user=User.objects.get(username=username)
                    if user.check_password(password):
                        if Token.objects.filter(user_id=user).exists():
                            token=Token.objects.get(user_id=user)
                        else:
                            token = Token.objects.create(user=user)
                        user.last_login = timezone.now()
                        user.save()
                        
    
                        return Response({
                                    "message": "you have successfully logged in",
                                    "status": True,
                                    "response": "success",
                                    "token": token.key,
                                    "data": {
                                        'username':user.username,
                                        'user_id': user.id,
                                        'email':user.email,
                                        "first_name": user.first_name,
                                        "last_name": user.last_name,
                                        }},
                                    status=status.HTTP_200_OK)
                    else:
                        return Response(
                            {"message": "You have entered an invalid password",
                                "status": False,
                                "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(
                            {"message": "You have entered an invalid username",
                                "status": False,
                                "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)
                            
                        
class AuthLogoutViewset(viewsets.ModelViewSet):
    authentication_classes = [cTokenAuthentication]
    permission_classes = [DjangoModelPermissions]
    queryset = User.objects.filter()
    http_method_names = ['post']    
    
    def create(self, request, *args, **kwargs):
        try:
            # Token.objects.get(user=request.user).delete()
            # Token.objects.create(user=request.user)
            logout(request)
            return Response({
                "message":"Logged out successfully",
                "status":True,
                "response":"success"
            },status=status.HTTP_200_OK)
        except Exception as error:
                return Response({
                        "message": str(error),
                        "status": False,
                        "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)
                   
            