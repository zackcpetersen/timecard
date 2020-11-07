import datetime
import pytz

from django.db import models

from accounts.models import User
from entries import constants


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entries')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    pause_time = models.DateTimeField(blank=True, null=True)
    time_paused = models.DurationField(default=datetime.timedelta())
    # paused = models.BooleanField(default=False)
    # project = models.ForeignKey(Project, related_name='entries)
    # location = models.ForeignKey(Location, related_name='entries)
    # entry_group = models.ForeignKey(EntryGroup) ???

    status = models.CharField(max_length=24,
                              choices=constants.ENTRY_STATUSES,
                              default=constants.UNVERIFIED)
    comments = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_worked = models.DurationField(default=datetime.timedelta())

    class Meta:
        verbose_name_plural = 'Entries'

    # def __str__(self):
    #     return '{} on {}'.format(self.user, self.project)

    def calculate_paused(self):
        if self.pause_time:
            time_paused = datetime.datetime.now(tz=pytz.UTC) - self.pause_time
            self.pause_time = None
            self.time_paused = time_paused
            self.save()
        # TODO raise exception

    def calculated_worked(self):
        if self.start_time and self.end_time:
            worked = self.end_time - self.time_paused - self.start_time
            self.time_worked = worked
            self.save()
        # TODO raise exception
