from django.shortcuts import render
from django_jinja_knockout.forms import Renderer
from django_jinja_knockout.viewmodels import vm_list
from django_jinja_knockout.views import ModelFormActionsView

from .forms import UserPreferencesForm


def renderer_test(request):
    renderer_child = Renderer(request, {
        'd': 4,
    })
    renderer_child.template = 'renderer_child.htm'
    renderer_top = Renderer(request, {
        'a': 1,
        'b': 2,
        'child': renderer_child,
        'c': 3,
    })
    renderer_top.template = 'renderer_top.htm'
    return render(request, 'renderer_test.htm', {'renderer_top': renderer_top})


class UserChangeView(ModelFormActionsView):

    form = UserPreferencesForm

    def action_edit_form(self, obj=None):
        if obj is None:
            obj = self.get_object_for_action()
        if self.request.user.is_superuser or obj == self.request.user:
            return super().action_edit_form(obj)
        else:
            return vm_list({
                'view': 'alert_error',
                'message': 'You do not have the rights to edit another user preferences.'
            })
