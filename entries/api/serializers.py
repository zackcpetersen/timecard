import pytz

from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from entries import constants as entry_constants
from entries.models import Entry
from projects.api.serializers import ProjectImageSerializer
from projects.models import Project


class EntryBaseSerializer(serializers.ModelSerializer):
    def time_paused_seconds (self, entry):
        return entry.time_paused.total_seconds()

    def time_worked_seconds(self, entry):
        return entry.time_worked.total_seconds()

    def get_project_name(self, entry):
        if entry.project:
            return Project.objects.get(pk=entry.project.pk).name

    def user_full_name(self, entry):
        return '{} {}'.format(entry.user.first_name, entry.user.last_name)

    def get_start_time(self, entry):
        if entry.start_time:
            return self.formatted_time(entry.start_time)

    def get_end_time(self, entry):
        if entry.end_time:
            return self.formatted_time(entry.end_time)

    def get_created_at(self, entry):
        return self.formatted_time(entry.created_at)

    def get_updated_at(self, entry):
        if entry.updated_at:
            return self.formatted_time(entry.updated_at)

    def formatted_time(self, time):
        local_tz = pytz.timezone('America/Denver')
        local_time = time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_time.strftime(entry_constants.DATETIME_NO_MICROSECOND)


class EntryCSVSerializer(EntryBaseSerializer):
    name = serializers.SerializerMethodField('user_full_name')
    project_name = serializers.SerializerMethodField('get_project_name')
    start_time = serializers.SerializerMethodField('get_start_time')
    end_time = serializers.SerializerMethodField('get_end_time')
    created_at = serializers.SerializerMethodField('get_created_at')
    updated_at = serializers.SerializerMethodField('get_updated_at')

    class Meta:
        model = Entry
        fields = ['id', 'name', 'start_time', 'end_time',
                  'time_paused', 'time_worked',
                  'project_name', 'status', 'comments',
                  'created_at', 'updated_at']


class EntrySerializer(EntryBaseSerializer):
    user = UserSerializer(read_only=True)
    entry_images = ProjectImageSerializer(many=True, read_only=True)
    time_paused_secs = serializers.SerializerMethodField('time_paused_seconds')
    time_worked_secs = serializers.SerializerMethodField('time_worked_seconds')
    project_name = serializers.SerializerMethodField('get_project_name')

    class Meta:
        model = Entry
        fields = entry_constants.ENTRY_ATTRS
