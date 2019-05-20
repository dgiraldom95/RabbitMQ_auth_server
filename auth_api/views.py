from rest_framework import viewsets, permissions
from rest_framework.permissions import BasePermission

from auth_api.models import *
from auth_api.serializers import *


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
