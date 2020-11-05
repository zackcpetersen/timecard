from django.forms import Form, ModelChoiceField

from accounts.models import User


class StartTimeForm(Form):
    user = ModelChoiceField(queryset=User.objects.all())
