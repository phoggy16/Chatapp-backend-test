from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from myapp.login.views import AuthLoginViewset
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from .views import AddMessageViewSet, GroupViewSet,AddUserViewSet, MessageLikerViewSet,SearchUserViewSet, ViewMessageViewSet
from .models import Group, Messages
# Create your tests here.
class TestClass(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user=User.objects.create(username='Master')
        self.user.set_password('123456')
        self.user.save()
        Token.objects.create(user=self.user)
    
    def test_user_login(self):
        
        view_create = AuthLoginViewset.as_view(actions={'post': 'create'})
        
        data = {    'username' :   "Master",
                    "password" : "123456",
                     }

        request = self.factory.post('/loginuser/', data)
        response = view_create(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_group(self):
        view_create = GroupViewSet.as_view(actions={'post': 'create'})
        data = {    "groupName":"group1"
                     }
        view_list = GroupViewSet.as_view(actions={'get': 'list'})
        viewupdate= GroupViewSet.as_view(actions={'put': 'update'})
        viewdelete= GroupViewSet.as_view(actions={'delete': 'destroy'})

        group=Group.objects.create(name="test",ref_user=self.user)

        requestCreate = self.factory.post('/creategroup/',data)
        force_authenticate(requestCreate, user=self.user, token=self.user.auth_token)
        response = view_create(requestCreate)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        requestList = self.factory.get('/getgroup/')
        force_authenticate(requestList, user=self.user, token=self.user.auth_token)
        response = view_list(requestList)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        requestUpdate = self.factory.put('/getupdate/',data)
        force_authenticate(requestUpdate, user=self.user, token=self.user.auth_token)
        response = viewupdate(requestUpdate,**{"pk":group.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        requestDelete = self.factory.delete('/deletegroup/')
        force_authenticate(requestDelete, user=self.user, token=self.user.auth_token)
        response = viewdelete(requestDelete,**{"pk":group.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_user(self):
        user=User.objects.create(username='hello')
        user.set_password('123456')
        user.save()

        group=Group.objects.create(name="test",ref_user=self.user)
        data = {    "groupId":group.id,
                    "memberId": user.id
                     }

        view_create = AddUserViewSet.as_view(actions={'post': 'create'})

        request=self.factory.post('/adduser/',data)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view_create(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search_user(self):
        
        data = {    "username":"rohit",

                     }

        view_create = SearchUserViewSet.as_view(actions={'post': 'create'})

        request=self.factory.post('/searchuser/',data)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view_create(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_message(self):

        group=Group.objects.create(name="test",ref_user=self.user)
        data = {    "groupId":group.id,
                    "message":"hello world"

                     }

        view_create = AddMessageViewSet.as_view(actions={'post': 'create'})

        request=self.factory.post('/addmessage/',data)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view_create(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_view_message(self):
        group=Group.objects.create(name="test",ref_user=self.user)
        data = {    "groupId":group.id

                     }

        view_create = ViewMessageViewSet.as_view(actions={'post': 'create'})

        request=self.factory.post('/viewmessage/',data)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view_create(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_liker_message(self):
        
        group=Group.objects.create(name="test",ref_user=self.user)
        message=Messages.objects.create(ref_user=self.user,ref_group=group,message="hello world")

        view_create = MessageLikerViewSet.as_view(actions={'post': 'create'})

        request=self.factory.post('/likemessage/',{"messageId":message.id})
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view_create(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        






