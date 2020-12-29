import datetime

from django.forms import BooleanField, ChoiceField, DateField, Form, ModelMultipleChoiceField

from accounts.models import User
from entries import constants
from entries.models import Entry
from projects.models import Project


class EntryFilterForm(Form):
    users = ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    projects = ModelMultipleChoiceField(queryset=Project.objects.all(), required=False)
    start_date = DateField(required=False)
    end_date = DateField(required=False)
    include_active_entries = BooleanField(required=False)
    include_all_users = BooleanField(required=False)

    def clean(self):
        if self.request_user and not self.cleaned_data.get('users'):
            self.cleaned_data['users'] = [self.request_user]
        # TODO might remove this - can just send all user pks in request, above would cover it
        if self.cleaned_data.get('include_all_users'):
            self.cleaned_data['users'] = User.objects.all()
        if not self.cleaned_data.get('start_date'):
            self.cleaned_data['start_date'] = datetime.date.today() - \
                                              datetime.timedelta(days=30)
            if not self.cleaned_data.get('end_date'):
                self.cleaned_data['end_date'] = datetime.date.today() + datetime.timedelta(days=1)
        if not self.cleaned_data.get('include_active_entries'):
            self.cleaned_data['include_active_entries'] = True

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.request_user = kwargs.get('user')
            kwargs.pop('user')
        super(EntryFilterForm, self).__init__(*args, **kwargs)


class EntryStatusForm(Form):
    entries = ModelMultipleChoiceField(queryset=Entry.objects.all())
    status = ChoiceField(choices=constants.ENTRY_STATUSES)

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.request_user = kwargs.get('user')
            kwargs.pop('user')
        super(EntryStatusForm, self).__init__(*args, **kwargs)
