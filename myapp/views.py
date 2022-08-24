from venv import create
from weakref import ref
from myapp.serializers import GroupSerializer, MessageSerializer
from .models import Group, Members, Messages, MessageLike
from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import transaction
from adminapp.serializers import UserSerializer
from myapp.authentication.authentication import cTokenAuthentication
from rest_framework.permissions import AllowAny
from django.utils import timezone
# Create your views here.

class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = [cTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Group.objects.all()
    serializer_class=GroupSerializer
    http_method_names = ['post','get','put','delete']

    def create(self, request, *args, **kwargs):
        try:
            data=request.data
            groupName=data['groupName']

            Group.objects.create(name=groupName,ref_user=request.user)

            return Response({"message":"group created successfully", "status": True,
                             "response": "success", }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

    
    def list(self, request, *args, **kwargs):
        try:
            data=self.serializer_class(self.queryset,many=True).data

            return Response({"data":data,"message":"group fetched successfully", "status": True,
                             "response": "success", }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            group=Group.objects.get(id=int(self.kwargs['pk']))
            group.name=request.data["groupName"]

            group.save()
            return Response({"message":"group updated successfully", "status": True,
                             "response": "success", }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            group=Group.objects.get(id=int(self.kwargs['pk']))
            if group.ref_user==request.user:
                group.delete()
            else:
                return Response({"message":"Group can not be deleted", "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"group deleted successfully", "status": True,
                             "response": "success", }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

class AddUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [cTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Group.objects.all()
    serializer_class=GroupSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            groupId=request.data['groupId']
            memberId=request.data['memberId']
            group=Group.objects.get(id=int(groupId))
            member=User.objects.get(id=int(memberId))

            if Members.objects.filter(ref_group=group,members=member).exists():
            
                return Response({"message":"member already exists", "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

            Members.objects.create(ref_group=group,members=member)

            return Response({"message":"member added successfully", "status": True,
                             "response": "success", }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)


class SearchUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [cTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class=UserSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            try:
                username=request.data['username']
                users=User.objects.filter(username__istartswith=username)
            except:
                users=User.objects.all()

            data=self.serializer_class(users,many=True).data
            
            return Response({"data":data,"message":"user fetched successfully", "status": True,
                             "response": "success", }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)


class AddMessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [cTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class=UserSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            groupId=request.data['groupId']
            message=request.data['message']

            group=Group.objects.get(id=int(groupId))

            Messages.objects.create(ref_user=request.user,ref_group=group,message=message)

            return Response({"message":"message added successfully", "status": True,
                             "response": "success", }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

class ViewMessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [cTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class=MessageSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            groupId=request.data['groupId']
            

            group=Group.objects.get(id=int(groupId))
            

            msg=Messages.objects.filter(ref_group=group)
            data=self.serializer_class(msg,many=True).data

            return Response({"data":data,"message":"message fetched successfully", "status": True,
                             "response": "success", }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)

    
class MessageLikerViewSet(viewsets.ModelViewSet):
    authentication_classes = [cTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = MessageLike.objects.all()
    serializer_class=[]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            messageId=request.data['messageId']
            

            msg=Messages.objects.get(id=int(messageId))
            
            if MessageLike.objects.filter(ref_message=msg,liked_by=request.user).exists():
                MessageLike.objects.get(ref_message=msg,liked_by=request.user).delete()
                msg="Message unliked successfully"
            else: 
                MessageLike.objects.create(ref_message=msg,liked_by=request.user)
                msg="message liked successfully"
            return Response({"message":msg, "status": True,
                             "response": "success", }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"message":str(error), "status": False,
                             "response": "fail", }, status=status.HTTP_400_BAD_REQUEST)
        


        