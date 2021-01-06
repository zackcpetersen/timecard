import datetime

from django.db.models import Q
from django.forms import BooleanField, ChoiceField, DateField, Form, ModelMultipleChoiceField, MultipleChoiceField

from accounts.models import User
from entries import constants
from entries.models import Entry
from projects.models import Project


class EntryFilterForm(Form):
    users = ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    projects = ModelMultipleChoiceField(queryset=Project.objects.all(), required=False)
    statuses = MultipleChoiceField(choices=constants.ENTRY_STATUSES, required=False)
    start_date = DateField(required=False)
    end_date = DateField(required=False)
    exclude_null_projects = BooleanField(required=False)
    include_active_entries = BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.request_user = kwargs.get('user')
            kwargs.pop('user')
        super(EntryFilterForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.cleaned_data.get('users'):
            self.cleaned_data['users'] = User.objects.all()
        if not self.cleaned_data.get('projects'):
            self.cleaned_data['projects'] = Project.objects.all()
        if not self.cleaned_data.get('statuses'):
            self.cleaned_data['statuses'] = [status[0] for status in constants.ENTRY_STATUSES]
        if not self.cleaned_data.get('start_date'):
            self.cleaned_data['start_date'] = datetime.date.today() - \
                                              datetime.timedelta(days=14)
        if not self.cleaned_data.get('end_date'):
            self.cleaned_data['end_date'] = datetime.date.today()
        if not self.cleaned_data.get('include_active_entries'):
            self.cleaned_data['include_active_entries'] = False

        entries = Entry.objects.filter(user__in=self.cleaned_data['users'],
                                       status__in=self.cleaned_data['statuses'],
                                       created_at__range=(self.cleaned_data['start_date'],
                                                          self.cleaned_data['end_date']),
                                       end_time__isnull=self.cleaned_data['include_active_entries'])
        entries = self.project_filter(entries)
        self.cleaned_data['entries'] = entries

    def clean_end_date(self):
        if self.cleaned_data['end_date']:
            if self.cleaned_data['end_date'] < self.cleaned_data['start_date']:
                self.add_error(error='Start Date must be before End Date!', field='end_date')

    def project_filter(self, entries):
        null_projects = not self.cleaned_data.get('exclude_null_projects')
        filters = Q(project__in=self.cleaned_data.get('projects')) | \
                 Q(project__isnull=null_projects)
        return entries.filter(filters)


class EntryStatusForm(Form):
    entries = ModelMultipleChoiceField(queryset=Entry.objects.all())
    status = ChoiceField(choices=constants.ENTRY_STATUSES)

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.request_user = kwargs.get('user')
            kwargs.pop('user')
        super(EntryStatusForm, self).__init__(*args, **kwargs)
