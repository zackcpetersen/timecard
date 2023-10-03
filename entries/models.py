import datetime
import pytz

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.api.gmail.gmail_service import GmailAPI
from accounts.models import User
from entries import constants
from entries import exceptions
from projects.constants import STATUS_ACTIVE
from projects.models import Project


@receiver(pre_save, sender='entries.Entry')
def check_project(sender, instance, **kwargs):
    if instance.start_time and instance.end_time:
        if not instance.project:
            raise exceptions.ProjectRequiredException()


pre_save.connect(check_project, sender='entries.Entry')


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
    status = models.CharField(max_length=24,
                              choices=constants.ENTRY_STATUSES,
                              default=constants.ACTIVE)
    comments = models.CharField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Entries'

    def __str__(self):
        return '{} on {}'.format(
            self.user, self.start_time)

    @staticmethod
    def email_unclosed():
        local_tz = pytz.timezone('America/Denver')
        today_timezone = datetime.datetime.today().replace(tzinfo=pytz.utc).astimezone(local_tz)
        today = today_timezone.replace(hour=0, minute=0, second=0, microsecond=0)
        unclosed = Entry.objects.filter(end_time__isnull=True, start_time__lt=today)

        for entry in unclosed:
            entry.status = constants.FLAGGED
            entry.end_time = entry.start_time + datetime.timedelta(hours=1)
            entry.time_paused = datetime.timedelta()
            if not entry.project:
                misc_proj = Project.objects.filter(name__icontains='misc').first()
                last_active_proj = Project.objects.filter(status=STATUS_ACTIVE).last()
                entry.project = misc_proj if misc_proj else last_active_proj
                if entry.comments:
                    entry.comments += constants.FLAGGED_ENTRY_COMMENT
                else:
                    entry.comments = constants.FLAGGED_ENTRY_COMMENT
            entry.save()
            email = GmailAPI()
            content = Entry.unclosed_entry_email_content(Entry.format_unclosed_entries(unclosed))
            message = email.create_email(settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_FROM_EMAIL,
                                         constants.FLAGGED_ENTRY_SUBJECT, content)
            email.send_email(message)

    @staticmethod
    def format_unclosed_entries(entries):
        return [constants.UNCLOSED_ENTRY_FORMAT.format(entry.user, entry.start_time) for entry in entries]

    @staticmethod
    def unclosed_entry_email_content(entries):
        return constants.UNCLOSED_ENTRY_CONTENT.format(entries, settings.DEFAULT_DOMAIN)

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

    def calculate_worked(self, save=True):
        if self.end_time:
            self.end_time = self.start_pause if not self.end_pause and self.start_pause else self.end_time
            self.time_worked = self.end_time - self.time_paused - self.start_time
            self.status = constants.NEEDS_APPROVAL if self.status != constants.FLAGGED else self.status
            if save:
                self.save()
        else:
            raise exceptions.FieldRequiredException('end_time')

    @staticmethod
    def get_datetime():
        return datetime.datetime.now(tz=pytz.UTC)


class EntryLocation(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='locations')
    loc_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    loc_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    loc_errors = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
