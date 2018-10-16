from django.contrib.auth.models import User

from django_jinja_knockout.forms import RendererModelForm


class UserPreferencesForm(RendererModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
