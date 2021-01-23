import datetime

from django.db.models import Sum, Q
from django.forms import BooleanField, ChoiceField, DateField, Form, ModelMultipleChoiceField, MultipleChoiceField

from accounts.models import User
from entries import constants
from entries.models import Entry
from projects.models import Project


class EntryDateForm(Form):
    start_date = DateField(required=False)
    end_date = DateField(required=False)

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

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.request_user = kwargs.get('user')
            kwargs.pop('user')
        super(EntryDateForm, self).__init__(*args, **kwargs)

    def clean_end_date(self):
        if self.cleaned_data['end_date']:
            if self.cleaned_data['end_date'] < self.cleaned_data['start_date']:
                self.add_error(error='Start Date must be before End Date!', field='end_date')
            return self.cleaned_data['end_date'] + datetime.timedelta(days=1)


class EntryCsvForm(EntryDateForm):
    users = ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    projects = ModelMultipleChoiceField(queryset=Project.objects.all(), required=False)
    statuses = MultipleChoiceField(choices=constants.ENTRY_STATUSES, required=False)
    null_projects = BooleanField(required=False)
    all_projects = BooleanField(required=False)

    def clean(self):
        if not self.cleaned_data.get('users'):
            self.cleaned_data['users'] = User.objects.all()
        if self.cleaned_data.get('all_projects'):
            self.cleaned_data['projects'] = Project.objects.all()
        if not self.cleaned_data.get('statuses'):
            self.cleaned_data['statuses'] = [status[0] for status in constants.ENTRY_STATUSES]

        entries = Entry.objects.filter(user__in=self.cleaned_data['users'],
                                       status__in=self.cleaned_data['statuses'],
                                       start_time__range=(self.cleaned_data['start_date'],
                                                          self.cleaned_data['end_date']))
        entries = self.project_filter(entries)
        self.cleaned_data['user_totals'] = self.user_totals(entries)
        self.cleaned_data['project_totals'] = self.project_totals(entries)
        self.cleaned_data['entries'] = entries

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
        hours = time_delta.seconds//3600
        minutes = (time_delta.seconds//60) % 60
        return '{}:{}'.format(hours, minutes)

    def project_filter(self, entries):
        null_projects = self.cleaned_data.get('null_projects')
        specific_projects = self.cleaned_data.get('projects')
        if null_projects and specific_projects:
            return entries.filter(Q(project__in=self.cleaned_data.get(
                'projects')) | Q(project__isnull=null_projects))
        if null_projects:
            entries = entries.filter(project__isnull=null_projects)
        if specific_projects:
            entries = entries.filter(project__in=specific_projects)
        return entries


class EntryStatusForm(Form):
    entries = ModelMultipleChoiceField(queryset=Entry.objects.all())
    status = ChoiceField(choices=constants.ENTRY_STATUSES)

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.request_user = kwargs.get('user')
            kwargs.pop('user')
        super(EntryStatusForm, self).__init__(*args, **kwargs)
