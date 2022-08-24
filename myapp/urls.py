from rest_framework import routers

from myapp.login.views import AuthLoginViewset, AuthLogoutViewset
from myapp.views import AddMessageViewSet, AddUserViewSet, GroupViewSet, MessageLikerViewSet, SearchUserViewSet, ViewMessageViewSet

router = routers.DefaultRouter()


router.register(r'login', AuthLoginViewset)
router.register(r'logout',AuthLogoutViewset)
router.register(r'group',GroupViewSet)
router.register(r'addUser',AddUserViewSet)
router.register(r'searchUser',SearchUserViewSet)
router.register(r'addMessage',AddMessageViewSet)
router.register(r'viewMessage',ViewMessageViewSet)
router.register(r'messageLiker',MessageLikerViewSet)