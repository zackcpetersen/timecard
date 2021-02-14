import pytz

from rest_framework import serializers

from accounts.api.serializers import UserCreationSerializer
from entries import constants as entry_constants
from entries.models import Entry
from projects.api.serializers import ProjectImageSerializer
from projects.models import Project


class EntryBaseSerializer(serializers.ModelSerializer):
    def get_time_paused_secs(self, entry):
        return entry.time_paused.total_seconds()

    def get_time_worked_secs(self, entry):
        return entry.time_worked.total_seconds()

    def get_project_name(self, entry):
        if entry.project:
            return Project.objects.get(pk=entry.project.pk).name

    def get_name(self, entry):
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
    name = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = ['id', 'name', 'start_time', 'end_time',
                  'time_paused', 'time_worked',
                  'project_name', 'status', 'comments',
                  'created_at', 'updated_at']


class EntrySerializer(EntryBaseSerializer):
    user = UserCreationSerializer(read_only=True)
    entry_images = ProjectImageSerializer(many=True, read_only=True)
    time_paused_secs = serializers.SerializerMethodField()
    time_worked_secs = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = entry_constants.ENTRY_ATTRS


class EntryUpdateSerializer(EntrySerializer):
    time_paused_secs = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()
    entry_images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Entry
        fields = ['id', 'start_time', 'end_time', 'start_pause', 'end_pause', 'end_time',
                  'project', 'project_name', 'time_paused_secs', 'entry_images']
