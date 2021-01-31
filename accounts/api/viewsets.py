from rest_framework import viewsets, views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.serializers import UserCreationSerializer, UserUpdateSerializer
from accounts.models import User
from accounts import permissions


class UserCreationViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for User CRUD
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, permissions.IsSuperuser]

    queryset = User.objects.all()
    serializer_class = UserCreationSerializer


class UserUpdateViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, permissions.ObjectOwnerOrSuperuserUpdate]

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class CurrentUserGetView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserUpdateSerializer(request.user)
        return Response(status=200, data=serializer.data)
