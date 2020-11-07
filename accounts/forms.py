from django.forms import Form, ModelChoiceField

from accounts.models import User


class UserForm(Form):
    user = ModelChoiceField(queryset=User.objects.all())
