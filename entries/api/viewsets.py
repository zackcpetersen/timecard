import datetime

from rest_framework import viewsets, views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from entries.api.serializers import EntrySerializer
from entries.constants import DATETIME_FORMAT
from entries.forms import StartTimeForm
from entries.models import Entry


class EntryViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Entry CRUD
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class StartTimeView(views.APIView):
    def post(self, request):
        form = StartTimeForm(request.data)
        if form.is_valid():
            user = form.cleaned_data['user']
            start_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
            entry = Entry.objects.create(user=user,
                                         start_time=start_time)
            serializer = EntrySerializer(entry)
            return Response(status=201, data=serializer.data)
        return Response(status=400, data=form.errors)
