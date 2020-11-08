import datetime
import pytz

from django.db import models

from accounts.models import User
from entries import constants
from entries.exceptions import FieldRequiredException, NullRequiredException


def update_time_paused(sender, instance, *args, **kwargs):
    if instance.end_pause and instance.start_pause:
        instance.calculate_paused()


def update_time_worked(sender, instance, *args, **kwargs):
    if instance.end_time:
        instance.calculate_worked()


models.signals.pre_save.connect(update_time_paused, sender='entries.Entry')
models.signals.pre_save.connect(update_time_worked, sender='entries.Entry')


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entries')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    start_pause = models.DateTimeField(blank=True, null=True)
    end_pause = models.DateTimeField(blank=True, null=True)
    time_paused = models.DurationField(default=datetime.timedelta())
    time_worked = models.DurationField(default=datetime.timedelta())
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

    class Meta:
        verbose_name_plural = 'Entries'

    # def __str__(self):
    #     return '{} on {}'.format(self.user, self.project)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.start_time = self.get_datetime()
        super(Entry, self).save(*args, **kwargs)

    def open_start(self, date_time=None):
        self.start_time = date_time
        self.save()

    def open_pause(self, date_time=None):
        start_pause = date_time if date_time else self.get_datetime()
        self.start_pause = start_pause
        self.save()

    def close_pause(self, date_time=None):
        end_pause = date_time if date_time else self.get_datetime()
        self.end_pause = end_pause
        self.save()

    def close_time(self, date_time=None):
        end_time = date_time if date_time else self.get_datetime()
        self.end_time = end_time
        self.save()

    def calculate_paused(self):
        if self.end_pause and self.start_pause:
            self.time_paused = self.end_pause - self.start_pause
        else:
            raise FieldRequiredException('[start_time, end_time]')

    def calculate_worked(self):
        if self.end_time:
            self.end_time = self.start_pause if not self.end_pause else self.get_datetime()
            self.time_worked = self.end_time - self.time_paused - self.start_time
            self.status = constants.NEEDS_APPROVAL
        else:
            raise FieldRequiredException('end_time')

    def auto_end_entry(self):
        if not self.end_time:
            today = self.get_datetime().strftime(constants.DATE_ONLY_FORMAT)
            entry_start_day = self.start_time.strftime(constants.DATE_ONLY_FORMAT)

            if entry_start_day == today:
                end_time = self.get_datetime()
            else:
                end_time = self.start_time.replace(hour=23, minute=59, second=59)

            self.end_time = end_time
            self.status = constants.FLAGGED
            self.save()
        else:
            raise NullRequiredException('end_time')

    @staticmethod
    def get_datetime():
        return datetime.datetime.now(tz=pytz.UTC)
