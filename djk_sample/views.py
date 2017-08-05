from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from django_jinja_knockout.views import ModelFormActionsView


class UserChangeView(ModelFormActionsView):

    model = User
    form = UserChangeForm
