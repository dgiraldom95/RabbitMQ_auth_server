from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from auth_api import views

router = DefaultRouter()
router.register(r'usuarios', views.UserViewSet)

urlpatterns = [
    url('token-auth/', obtain_jwt_token),
    url('token-verify/', verify_jwt_token),
    path('', include(router.urls))
]
