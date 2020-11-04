from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from entries.api.serializers import EntrySerializer
from entries.models import Entry


class EntryViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Entry CRUD
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
