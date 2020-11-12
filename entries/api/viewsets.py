from rest_framework import viewsets, views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.forms import StartTimeForm, UserForm
from entries.api.serializers import EntrySerializer
from entries.exceptions import FieldRequiredException, NullRequiredException
from entries.models import Entry


class EntryViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Entry CRUD
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


# TODO add authentication on all views - Mixin?
class StartTimeView(views.APIView):
    def post(self, request):
        form = StartTimeForm(request.data)
        if form.is_valid():
            user = form.cleaned_data['user']
            last_entry = form.cleaned_data.get('last_entry')
            if last_entry and not last_entry.end_time:
                last_entry.auto_end_entry()
            entry = Entry.objects.create(user=user)
            serializer = EntrySerializer(entry)
            return Response(status=201, data=serializer.data)
        return Response(status=400, data=form.errors)


class EndTimeView(views.APIView):
    def post(self, request):
        form = UserForm(request.data)
        if form.is_valid():
            entry = form.cleaned_data['last_entry']
            entry.close_time()
            serializer = EntrySerializer(entry)
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=form.errors)


class StartPauseView(views.APIView):
    def post(self, request):
        form = UserForm(request.data)
        if form.is_valid():
            entry = form.cleaned_data['last_entry']
            if not entry.start_pause:
                entry.open_pause()
                serializer = EntrySerializer(entry)
                return Response(status=200, data=serializer.data)
            raise NullRequiredException('Pause Time')
        return Response(status=400, data=form.errors)


class EndPauseView(views.APIView):
    def post(self, request):
        form = UserForm(request.data)
        if form.is_valid():
            entry = form.cleaned_data['last_entry']
            if entry.start_pause:
                entry.close_pause()
                serializer = EntrySerializer(entry)
                return Response(status=200, data=serializer.data)
            raise FieldRequiredException('pause_time')
        return Response(status=400, data=form.errors)
