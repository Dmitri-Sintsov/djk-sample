from django.contrib.auth.models import User

from django_jinja_knockout.viewmodels import vm_list
from django_jinja_knockout.views import ModelFormActionsView

from .forms import UserPreferencesForm


class UserChangeView(ModelFormActionsView):

    form = UserPreferencesForm

    def action_edit_form(self):
        obj = self.get_object_for_action()
        if self.request.user.is_superuser or obj == self.request.user:
            return super().action_edit_form(obj)
        else:
            return vm_list({
                    'view': 'alert_error',
                    'message': 'You do not have the rights to edit another user preferences.'
                }
            )
