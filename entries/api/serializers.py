from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from entries.models import Entry
from projects.api.serializers import ProjectImageSerializer
from projects.models import Project


class EntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    entry_images = ProjectImageSerializer(many=True, read_only=True)
    time_paused_secs = serializers.SerializerMethodField('time_paused_seconds')
    time_worked_secs = serializers.SerializerMethodField('time_worked_seconds')
    project_name = serializers.SerializerMethodField('get_project_name')

    class Meta:
        model = Entry
        fields = ['id', 'user', 'start_time', 'end_time', 'start_pause', 'end_pause',
                  'time_paused', 'time_paused_secs', 'time_worked', 'time_worked_secs', 'project',
                  'project_name', 'status', 'comments', 'created_at', 'updated_at',
                  'entry_images']

    def time_paused_seconds (self, entry):
        return entry.time_paused.total_seconds()

    def time_worked_seconds(self, entry):
        return entry.time_worked.total_seconds()

    def get_project_name(self, entry):
        if entry.project:
            return Project.objects.get(pk=entry.project.pk).name
