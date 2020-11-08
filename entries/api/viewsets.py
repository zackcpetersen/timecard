import datetime
import pytz

from rest_framework import viewsets, views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.forms import StartTimeForm, UserForm
from entries.api.serializers import EntrySerializer
from entries import constants
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


class StartTimeView(views.APIView):
    def post(self, request):
        form = UserForm(request.data)
        if form.is_valid():
            user = form.cleaned_data['user']
            last_entry = user.entries.last()
            if last_entry and not last_entry.end_time:
                # TODO possibly able to inherit this functionality - or mixin
                # TODO may want to do a day check as well (check if new entry is same day as previous)
                last_entry.end_time = last_entry.start_time.replace(hour=23, minute=59, second=59)
                last_entry.status = constants.NEEDS_APPROVAL
                last_entry.save()
            start_time = datetime.datetime.now(tz=pytz.UTC)
            entry = Entry.objects.create(user=user,
                                         start_time=start_time)
            serializer = EntrySerializer(entry)
            return Response(status=201, data=serializer.data)
        return Response(status=400, data=form.errors)


class EndTimeView(views.APIView):
    def post(self, request):
        form = UserForm(request.data)
        if form.is_valid():
            entry = form.cleaned_data['user'].entries.last()
            entry.calculated_worked()
            serializer = EntrySerializer(entry)
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=form.errors)


class StartPauseView(views.APIView):
    def post(self, request):
        form = UserForm(request.data)
        if form.is_valid():
            entry = form.cleaned_data['user'].entries.last()
            # TODO handle null entry elsewhere on all these views
            if entry and not entry.pause_time:
                entry.pause_time = datetime.datetime.now(tz=pytz.UTC)
                entry.save()
                serializer = EntrySerializer(entry)
                return Response(status=200, data=serializer.data)
            raise NullRequiredException('Pause Time')
        return Response(status=400, data=form.errors)


class EndPauseView(views.APIView):
    def post(self, request):
        form = UserForm(request.data)
        if form.is_valid():
            entry = form.cleaned_data['user'].entries.last()
            if entry and entry.pause_time:
                entry.calculate_paused()
                serializer = EntrySerializer(entry)
                return Response(status=200, data=serializer.data)
            raise FieldRequiredException('Pause Time')
        return Response(status=400, data=form.errors)
