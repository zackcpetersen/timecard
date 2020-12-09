from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from entries.models import Entry


class EntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    time_paused = serializers.SerializerMethodField('time_paused_seconds')
    time_worked = serializers.SerializerMethodField('time_worked_seconds')

    class Meta:
        model = Entry
        fields = '__all__'

    def time_paused_seconds (self, entry):
        return entry.time_paused.total_seconds()

    def time_worked_seconds(self, entry):
        return entry.time_worked.total_seconds()
