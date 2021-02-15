from django.db.models.deletion import ProtectedError
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from timecard.exceptions import DeletionException


class DeletionView(viewsets.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        try:
            return super(DeletionView, self).destroy(request, *args, **kwargs)
        except ProtectedError as e:
            raise DeletionException(e)


class AuthenticatedAPIView(DeletionView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
