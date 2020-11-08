from django.forms import Form, ModelChoiceField

from accounts.models import User


class StartTimeForm(Form):
    user = ModelChoiceField(queryset=User.objects.all())

    def clean_user(self):
        if self.cleaned_data.get('user').entries.count():
            self.cleaned_data['last_entry'] = self.cleaned_data['user'].entries.last()
        return self.cleaned_data['user']


class UserForm(Form):
    user = ModelChoiceField(queryset=User.objects.all())

    def clean_user(self):
        if self.cleaned_data.get('user').entries.count():
            self.cleaned_data['last_entry'] = self.cleaned_data['user'].entries.last()
            return self.cleaned_data['user']
        msg = '{} has no entries!'.format(self.cleaned_data['user'])
        self.add_error('user', msg)
