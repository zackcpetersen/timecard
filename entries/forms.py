import datetime

from django.db.models import Sum, Q
from django.forms import ChoiceField, DateField, Form, ModelMultipleChoiceField

from accounts.models import User
from entries import constants
from entries.models import Entry
from projects.models import Project


class EntryDateForm(Form):
    start_date = DateField(required=False)
    end_date = DateField(required=False)

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.request_user = kwargs.get('user')
            kwargs.pop('user')
        super(EntryDateForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.cleaned_data.get('start_date'):
            self.cleaned_data['start_date'] = datetime.date.today() - \
                                              datetime.timedelta(days=14)
        if not self.cleaned_data.get('end_date'):
            self.cleaned_data['end_date'] = datetime.date.today() + datetime.timedelta(days=1)

        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        user = self.request_user

        entries = Entry.objects.filter(start_time__range=(
            start_date, end_date)).order_by('-start_time')
        if not user.is_admin:
            entries = entries.filter(user=user)
        self.cleaned_data['entries'] = entries

    def clean_end_date(self):
        if self.cleaned_data['end_date']:
            if self.cleaned_data['end_date'] < self.cleaned_data['start_date']:
                self.add_error(error='Start Date must be before End Date!', field='end_date')
            return self.cleaned_data['end_date'] + datetime.timedelta(days=1)


class EntryCsvForm(Form):
    entries = ModelMultipleChoiceField(queryset=Entry.objects.all())

    def clean(self):
        entries = self.cleaned_data['entries']
        self.cleaned_data['users'] = User.objects.filter(pk__in=entries.values_list('user__pk', flat=True))
        self.cleaned_data['projects'] = Project.objects.filter(pk__in=entries.values_list('project__pk', flat=True))
        self.cleaned_data['user_totals'] = self.user_totals(entries)
        self.cleaned_data['project_totals'] = self.project_totals(entries)
        self.cleaned_data['now'] = datetime.datetime.now()

    def user_totals(self, entries):
        user_totals = [['User', 'Hours Worked']]
        for user in self.cleaned_data['users']:
            hours_total = entries.aggregate(hours_total=Sum(
                'time_worked', filter=Q(user=user))).get('hours_total')
            user_name = '{} {}'.format(user.first_name, user.last_name)
            user_totals.append([user_name, self.format_timedelta(hours_total)])

        return user_totals

    def project_totals(self, entries):
        proj_totals = [['Project', 'Hours Worked']]
        for proj in self.cleaned_data['projects']:
            hours_total = entries.aggregate(hours_total=Sum(
                'time_worked', filter=Q(project=proj))).get('hours_total')
            proj_totals.append([proj.name, self.format_timedelta(hours_total)])

        return proj_totals

    @staticmethod
    def format_timedelta(time_delta):
        return str(time_delta).split('.')[0] if time_delta else '0:00:00'


class EntryStatusForm(Form):
    entries = ModelMultipleChoiceField(queryset=Entry.objects.all())
    status = ChoiceField(choices=constants.ENTRY_STATUSES)

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.request_user = kwargs.get('user')
            kwargs.pop('user')
        super(EntryStatusForm, self).__init__(*args, **kwargs)
