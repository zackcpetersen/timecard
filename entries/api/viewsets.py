import csv

from django.http import HttpResponse
from rest_framework import views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.forms import StartTimeForm, UserForm
from accounts import permissions
from entries.api.serializers import EntryCSVSerializer, EntryLocationSerializer, \
    EntrySerializer
from entries import constants as entry_constants
from entries.exceptions import FieldRequiredException, NullRequiredException
from entries.forms import EntryDateForm, EntryCsvForm, EntryStatusForm
from entries.models import Entry, EntryLocation
from timecard.viewsets import AuthenticatedAPIViewSet


class EntryViewSet(AuthenticatedAPIViewSet):
    """
    API Endpoint for Entry CRUD
    """
    permission_classes = [IsAuthenticated, permissions.ObjectOwnerReadOnlyAdminEdit]

    queryset = Entry.objects.all().order_by('-start_time')
    serializer_class = EntrySerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return self.queryset
        return self.queryset.filter(user=self.request.user)


class EntryUpdateViewSet(EntryViewSet):
    permission_classes = [IsAuthenticated, permissions.ObjectOwnerOrAdminUpdate]
    serializer_class = EntrySerializer


class EntryOwnerViewSet(EntryUpdateViewSet):
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AuthenticatedApiView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


class EntryLocationViewSet(AuthenticatedAPIViewSet):
    queryset = EntryLocation.objects.all()
    serializer_class = EntryLocationSerializer


class EntryStatusView(AuthenticatedApiView):
    def post(self, request):
        user = request.user
        form = EntryStatusForm(request.data, user=user)
        if form.is_valid():
            entries = form.cleaned_data['entries']
            status = form.cleaned_data['status']
            for entry in entries:
                if entry.status != 'active':
                    entry.status = status
                    entry.save()
            serializer = EntrySerializer(entries, many=True)
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=form.errors)


class StartTimeView(AuthenticatedApiView):
    """
    API endpoint to create and start an entry
    """
    def post(self, request):
        request.data['user'] = request.user
        form = StartTimeForm(request.data)
        if form.is_valid():
            user = form.cleaned_data['user']
            last_entry = form.cleaned_data.get('last_entry')
            if last_entry and not last_entry.end_time:
                last_entry.auto_end_entry()
            entry = Entry.objects.create(user=user)
            entry.open_start()
            serializer = EntrySerializer(entry)
            return Response(status=201, data=serializer.data)
        return Response(status=400, data=form.errors)


class EndTimeView(AuthenticatedApiView):
    """
    API endpoint to set end time and close an entry
    """
    def post(self, request):
        if request.user and not request.data.get('user'):
            request.data['user'] = request.user
        form = UserForm(request.data)
        if form.is_valid():
            entry = form.cleaned_data['last_entry']
            entry.close_time()
            serializer = EntrySerializer(entry)
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=form.errors)


class StartPauseView(AuthenticatedApiView):
    """
    API endpoint to start pause time on an entry
    """
    def post(self, request):
        if request.user and not request.data.get('user'):
            request.data['user'] = request.user
        form = UserForm(request.data)
        if form.is_valid():
            entry = form.cleaned_data['last_entry']
            if not entry.start_pause:
                entry.open_pause()
                serializer = EntrySerializer(entry)
                return Response(status=200, data=serializer.data)
            raise NullRequiredException('Pause Time')
        return Response(status=400, data=form.errors)


class EndPauseView(AuthenticatedApiView):
    """
    API endpoint to set end pause time and calculate paused time
    """
    def post(self, request):
        if request.user and not request.data.get('user'):
            request.data['user'] = request.user
        form = UserForm(request.data)
        if form.is_valid():
            entry = form.cleaned_data['last_entry']
            if entry.start_pause:
                entry.close_pause()
                serializer = EntrySerializer(entry)
                return Response(status=200, data=serializer.data)
            raise FieldRequiredException('pause_time')
        return Response(status=400, data=form.errors)


class EntryFilterView(AuthenticatedApiView):
    """
    API endpoint to get entries within a given date range
    """
    def post(self, request):
        form = EntryDateForm(request.data, user=request.user)
        if form.is_valid():
            entries = form.cleaned_data.get('entries')

            serializer = EntrySerializer(entries, many=True)
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=form.errors)


class EntryCSVDownloadView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, permissions.CustomAdminUser]

    def post(self, request):
        form = EntryCsvForm(request.data)
        if form.is_valid():
            filename = 'entries_{}-{}'.format(form.cleaned_data['start_date'],
                                              form.cleaned_data['end_date'])
            entries = EntryCSVSerializer(form.cleaned_data['entries'], many=True)
            rows = form.cleaned_data['user_totals']
            rows += form.cleaned_data['project_totals']
            rows += [entry_constants.ENTRY_CSV_ATTRS]
            rows += [entry.values() for entry in entries.data]
            return self.create_csv(entry_constants.ENTRY_CSV_ATTRS, rows, filename)
        return Response(status=400, data=form.errors)

    def create_csv(self, headers, rows, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        writer = csv.writer(response)
        # writer.writerow(headers)
        for row in rows:
            writer.writerow(row)

        return response
