from rest_framework import routers

from adminapp.views import UserViewSet, adminLogin

router = routers.DefaultRouter()


router.register(r'user', UserViewSet),
router.register(r'login',adminLogin)