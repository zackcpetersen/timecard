from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from accounts.api.serializers import UserSerializer
from accounts.models import User
from accounts import permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for User CRUD
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, permissions.ObjectOwnerOrSuperuserUpdate]

    queryset = User.objects.all()
    serializer_class = UserSerializer
