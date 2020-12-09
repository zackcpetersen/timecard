from django.forms import Form, ModelChoiceField, ModelMultipleChoiceField, DateField

from accounts.exceptions import InvalidDateRangeException
from accounts.models import User


class StartTimeForm(Form):
    user = ModelChoiceField(queryset=User.objects.all(), required=False)

    def clean_user(self):
        if self.cleaned_data.get('user').entries.count():
            self.cleaned_data['last_entry'] = self.cleaned_data['user'].entries.last()
        return self.cleaned_data['user']


class UserForm(Form):
    user = ModelChoiceField(queryset=User.objects.all(), required=False)

    def clean_user(self):
        if self.cleaned_data.get('user').entries.count():
            self.cleaned_data['last_entry'] = self.cleaned_data['user'].entries.last()
            return self.cleaned_data['user']
        msg = '{} has no entries!'.format(self.cleaned_data['user'])
        self.add_error('user', msg)


class MultiUserForm(Form):
    users = ModelMultipleChoiceField(queryset=User.objects.all())
    start_date = DateField()
    end_date = DateField()

    def clean(self):
        if self.cleaned_data.get('start_date') > self.cleaned_data.get('end_date'):
            raise InvalidDateRangeException(self.cleaned_data['start_date'], self.cleaned_data['end_date'])
