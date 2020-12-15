import copy
import csv

from django.http import HttpResponse
from rest_framework import viewsets, views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.forms import MultiUserForm, StartTimeForm, UserForm
from entries.api.serializers import EntrySerializer
from entries.exceptions import FieldRequiredException, NullRequiredException
from entries.forms import EntryFilterForm
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
class EntryFilterView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user if request.user else None
        form = EntryFilterForm(request.data, user=user)
        if form.is_valid():
            entries = Entry.objects.all()
            if form.cleaned_data.get('projects'):
                entries = entries.filter(project__in=form.cleaned_data['projects'])
            if not form.cleaned_data['include_active_entries']:
                entries.exclude(end_time__null=True)
            entries = entries.filter(user__in=form.cleaned_data['users'],
                                     start_time__range=(form.cleaned_data['start_date'],
                                                        form.cleaned_data['end_date']))

            serializer = EntrySerializer(entries, many=True)
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=form.errors)


class StartTimeView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = copy.deepcopy(request.data)
        if request.user:
            data.update({'user': request.user})
        form = StartTimeForm(data)
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


class EndTimeView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = copy.deepcopy(request.data)
        if request.user:
            data.update({'user': request.user})
        form = UserForm(data)
        if form.is_valid():
            entry = form.cleaned_data['last_entry']
            entry.close_time()
            serializer = EntrySerializer(entry)
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=form.errors)


class StartPauseView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = copy.deepcopy(request.data)
        if request.user:
            data.update({'user': request.user})
        form = UserForm(data)
        if form.is_valid():
            entry = form.cleaned_data['last_entry']
            if not entry.start_pause:
                entry.open_pause()
                serializer = EntrySerializer(entry)
                return Response(status=200, data=serializer.data)
            raise NullRequiredException('Pause Time')
        return Response(status=400, data=form.errors)


class EndPauseView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = copy.deepcopy(request.data)
        if request.user:
            data.update({'user': request.user})
        form = UserForm(data)
        if form.is_valid():
            entry = form.cleaned_data['last_entry']
            if entry.start_pause:
                entry.close_pause()
                serializer = EntrySerializer(entry)
                return Response(status=200, data=serializer.data)
            raise FieldRequiredException('pause_time')
        return Response(status=400, data=form.errors)


class EntryCSVDownloadView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = MultiUserForm(request.data)
        if form.is_valid():
            users = form.cleaned_data['users']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            return self.create_csv(users, start_date, end_date)
        return Response(status=400, data=form.errors)

    def create_csv(self, users, start_date, end_date):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=entries_{}-{}.csv'.format(start_date, end_date)
        writer = csv.writer(response)
        headers = ['Name', 'Date', 'Project', 'Clock-In', 'Clock-Out', 'Start-Pause', 'End-Pause', 'Time-Paused', 'Time-Worked']
        writer.writerow(headers)
        for user in users:
            for entry in user.entries.filter(created_at__range=(start_date, end_date)):
                data = [user.email, entry.created_at, entry.project, entry.start_time, entry.end_time,
                        entry.start_pause, entry.end_pause, entry.time_paused, entry.time_worked]
                entry_data = self.csv_no_null_vals(data)
                writer.writerow(entry_data)
        return response

    def csv_no_null_vals(self, vals):
        complete = []
        for val in vals:
            if not val:
                val = ' '
            else:
                val = val
            complete.append(val)

        return complete
