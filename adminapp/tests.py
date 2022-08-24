from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from .views import UserViewSet,adminLogin
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
# Create your tests here.
class UserCreateTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user=User.objects.create(username='admin')
        self.user.set_password('123456')
        self.user.is_superuser=1
        self.user.save()
        Token.objects.create(user=self.user)
    
    # for admin login
    def test_admin_login(self):
        
        view_create = adminLogin.as_view(actions={'post': 'create'})
        
        data = {    'username' :   "admin",
                    "password" : "123456",
                     }

        request = self.factory.post('/loginadmin/', data)
        
        response = view_create(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # for create user
    def test_create_user(self):
        view_create = UserViewSet.as_view(actions={'post': 'create'})
        data = {    'username' :   "rohit",
                    "password" : "123456",
                    "first_name" : "rohit",
                    "last_name" : "phogat",
                    "email":"rohit@yopmail.com"
                     }
        requestCreate = self.factory.post('/User/',data)
        force_authenticate(requestCreate, user=self.user, token=self.user.auth_token)

        
        response = view_create(requestCreate)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_user(self):
        view_update = UserViewSet.as_view(actions={'put': 'update'})

        data = { 
                    "password" : "1234567",
                    "first_name" : "rohit",
                    "last_name" : "phogat",
                    "email":"rohit@yopmail.com"
                     }

        request = self.factory.put('/updateUser/',data)
        force_authenticate(request, user=self.user, token=self.user.auth_token)

        response = view_update(request,**{"pk": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)