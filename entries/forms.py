import datetime
import pytz

from django.db.models import Sum, Q
from django.forms import CharField, ChoiceField, DateField, DateTimeField, Form, ModelMultipleChoiceField

from accounts.models import User
from entries import constants
from entries.models import Entry
from entries.utils import format_timedelta
from projects.models import Project


class EntryDateForm(Form):
    start_date = DateTimeField(required=False)
    end_date = DateTimeField(required=False)
    timezone = CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.request_user = kwargs.get('user')
            kwargs.pop('user')
        super(EntryDateForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.errors:
            today = datetime.datetime.now(tz=self.cleaned_data.get('timezone'))

            if not self.cleaned_data.get('start_date'):
                self.cleaned_data['start_date'] = today - datetime.timedelta(days=14)
            if not self.cleaned_data.get('end_date'):
                self.cleaned_data['end_date'] = today + datetime.timedelta(days=1)

            start_date = self.cleaned_data['start_date'].replace(
                hour=23, minute=59, second=59, tzinfo=self.cleaned_data.get('timezone'))
            end_date = self.cleaned_data['end_date'].replace(
                hour=23, minute=59, second=59, tzinfo=self.cleaned_data.get('timezone'))

            entries = Entry.objects.filter(start_time__range=(
                start_date, end_date)).order_by('-start_time').select_related(
                'user', 'project').prefetch_related('locations', 'entry_images')
            if not self.request_user.is_admin:
                entries = entries.filter(user=self.request_user)
            self.cleaned_data['entries'] = entries

    def clean_end_date(self):
        if not self.errors:
            if self.cleaned_data.get('start_date'):
                if self.cleaned_data['end_date'] < self.cleaned_data['start_date']:
                    self.add_error(error='Start Date must be before End Date!', field='end_date')
                return self.cleaned_data.get('end_date') + datetime.timedelta(days=1)

    def clean_timezone(self):
        tz = None
        try:
            tz = pytz.timezone(self.cleaned_data.get('timezone'))
        except pytz.exceptions.UnknownTimeZoneError:
            self.add_error('timezone', '{} is an invalid timezone'.format(self.cleaned_data['timezone']))
        return tz


class EntryCsvForm(Form):
    start_date = DateField()
    end_date = DateField()
    entries = ModelMultipleChoiceField(queryset=Entry.objects.all())

    def clean_entries(self):
        return self.cleaned_data['entries'].exclude(status=constants.ACTIVE)

    def clean(self):
        entries = self.cleaned_data['entries']
        self.cleaned_data['users'] = User.objects.filter(pk__in=entries.values_list('user__pk', flat=True))
        self.cleaned_data['projects'] = Project.objects.filter(pk__in=entries.values_list('project__pk', flat=True))
        self.cleaned_data['date_range'] = [['Entries for {} - {}'.format(self.cleaned_data['start_date'],
                                                                         self.cleaned_data['end_date'])]]
        self.cleaned_data['user_totals'] = self.user_totals(entries)
        self.cleaned_data['project_totals'] = self.project_totals(entries)
        self.cleaned_data['now'] = datetime.datetime.now()

    def user_totals(self, entries):
        user_totals = [['User', 'Hours Worked']]
        for user in self.cleaned_data['users']:
            hours_total = entries.aggregate(hours_total=Sum(
                'time_worked', filter=Q(user=user))).get('hours_total')
            user_name = '{} {}'.format(user.first_name, user.last_name)
            user_totals.append([user_name, format_timedelta(hours_total)])

        return user_totals

    def project_totals(self, entries):
        proj_totals = [['Project', 'Hours Worked']]
        for proj in self.cleaned_data['projects']:
            hours_total = entries.aggregate(hours_total=Sum(
                'time_worked', filter=Q(project=proj))).get('hours_total')
            proj_totals.append([proj.name, format_timedelta(hours_total)])

        return proj_totals


class EntryStatusForm(Form):
    entries = ModelMultipleChoiceField(queryset=Entry.objects.exclude(status=constants.ACTIVE))
    status = ChoiceField(choices=constants.ENTRY_STATUSES)

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.request_user = kwargs.get('user')
            kwargs.pop('user')
        super(EntryStatusForm, self).__init__(*args, **kwargs)
