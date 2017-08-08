from django.contrib.auth.models import User

from django_jinja_knockout.views import ModelFormActionsView

from .forms import UserPreferencesForm


class UserChangeView(ModelFormActionsView):

    form = UserPreferencesForm
