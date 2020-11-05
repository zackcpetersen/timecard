from django.db import models

from accounts.models import User
from entries import constants


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entries')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    seconds_paused = models.PositiveIntegerField(default=0)
    pause_time = models.DateTimeField(blank=True, null=True)
    paused = models.BooleanField(default=False)
    # project = models.ForeignKey(Project, related_name='entries)
    # location = models.ForeignKey(Location, related_name='entries)
    # entry_group = models.ForeignKey(EntryGroup) ???

    status = models.CharField(max_length=24,
                              choices=constants.ENTRY_STATUSES,
                              default=constants.UNVERIFIED)
    comments = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hours = models.DecimalField(max_digits=11, decimal_places=5, default=0)

    # def __str__(self):
    #     return '{} on {}'.format(self.user, self.project)
