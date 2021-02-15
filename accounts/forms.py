from django.forms import CharField, EmailField, Form, ModelChoiceField

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


class UserResetPasswordForm(Form):
    new_password = CharField(max_length=99)
    confirm_password = CharField(max_length=99)

    def clean(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            msg = 'Both passwords must match!'
            self.add_error('confirm_password', msg)
        else:
            self.cleaned_data['password'] = self.cleaned_data['new_password']


class ForgotPasswordForm(Form):
    email = EmailField()

    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data['email']).first()
        if user:
            self.cleaned_data['user'] = user
            return self.cleaned_data['email']

        msg = '{} is not associated to an account!'.format(self.cleaned_data['email'])
        self.add_error('email', msg)
