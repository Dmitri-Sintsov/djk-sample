from django.contrib.auth.models import User

from django_jinja_knockout.forms import BootstrapModelForm


class UserPreferencesForm(BootstrapModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
