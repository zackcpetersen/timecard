import datetime
import pytz

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import User
from entries import constants
from entries import exceptions
from projects.models import Project


# @receiver(pre_save, sender='entries.Entry')
# def check_project(sender, instance, **kwargs):
#     if instance.start_time and instance.end_time:
#         if not instance.project:
#             raise exceptions.ProjectRequiredException()
#
#
# pre_save.connect(check_project, sender='entries.Entry')


@receiver(pre_save, sender='entries.Entry')
def manual_entry_changes(sender, instance, **kwargs):
    if instance.end_time:
        if instance.start_time > instance.end_time:
            raise exceptions.EndTimeException()
        expected_time_worked = instance.end_time - instance.start_time - instance.time_paused
        if instance.time_paused > instance.end_time - instance.start_time:
            raise exceptions.TimeWorkedException()
        if expected_time_worked != instance.time_worked:
            instance.start_pause, instance.end_pause = None, None
            instance.calculate_worked()
    if instance.end_time and instance.status == constants.ACTIVE:
        instance.status = constants.NEEDS_APPROVAL


pre_save.connect(manual_entry_changes, sender='entries.Entry')


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entries')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    start_pause = models.DateTimeField(blank=True, null=True)
    end_pause = models.DateTimeField(blank=True, null=True)
    time_paused = models.DurationField(default=datetime.timedelta())
    time_worked = models.DurationField(default=datetime.timedelta())
    project = models.ForeignKey(Project,
                                on_delete=models.PROTECT,
                                related_name='entries',
                                null=True,
                                blank=True)
    # location = models.ForeignKey(Location, related_name='entries)
    # entry_group = models.ForeignKey(EntryGroup) ???

    status = models.CharField(max_length=24,
                              choices=constants.ENTRY_STATUSES,
                              default=constants.ACTIVE)
    comments = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Entries'

    # def __str__(self):
    #     return '{} on {}'.format(self.user, self.project)

    def open_start(self, date_time=None):
        self.start_time = date_time if date_time else self.get_datetime()
        self.save()

    def open_pause(self, date_time=None):
        start_pause = date_time if date_time else self.get_datetime()
        self.start_pause = start_pause
        self.save()

    def close_pause(self, date_time=None):
        end_pause = date_time if date_time else self.get_datetime()
        self.end_pause = end_pause
        self.calculate_paused()
        self.start_pause, self.end_pause = None, None
        self.save()

    def close_time(self, date_time=None):
        self.end_time = date_time if date_time else self.get_datetime()
        self.status = constants.NEEDS_APPROVAL
        self.calculate_worked()

    def calculate_paused(self):
        if self.end_pause and self.start_pause:
            time_paused = self.end_pause - self.start_pause
            self.time_paused += time_paused
            self.save()
        else:
            raise exceptions.FieldRequiredException('[start_time, end_time]')

    def calculate_worked(self):
        if self.end_time:
            self.end_time = self.start_pause if not self.end_pause and self.start_pause else self.end_time
            self.time_worked = self.end_time - self.time_paused - self.start_time
            self.status = constants.NEEDS_APPROVAL
            self.save()
        else:
            raise exceptions.FieldRequiredException('end_time')

    def auto_end_entry(self):
        if not self.end_time:
            today = self.get_datetime().strftime(constants.DATE_ONLY_FORMAT)
            entry_start_day = self.start_time.strftime(constants.DATE_ONLY_FORMAT)

            if entry_start_day == today:
                end_time = self.get_datetime()
            else:
                end_time = None

            self.end_time = end_time
            self.status = constants.FLAGGED
            self.save()
        else:
            raise exceptions.NullRequiredException('end_time')

    @staticmethod
    def get_datetime():
        return datetime.datetime.now(tz=pytz.UTC)
