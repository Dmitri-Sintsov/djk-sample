from django.shortcuts import render
from django_jinja_knockout import tpl
from django_jinja_knockout.viewmodels import vm_list
from django_jinja_knockout.views import create_template_context, ModelFormActionsView

from .forms import UserPreferencesForm


def renderer_test(request, **kwargs):
    # Test template_context without decorator.
    create_template_context(request)
    renderer_child = tpl.Renderer(request, {
        'd': 4,
    })
    renderer_child.template = 'child.htm'
    renderer_top = tpl.Renderer(request, {
        'a': 1,
        'b': 2,
        'child': renderer_child,
        'c': 3,
    })
    renderer_top.template = 'top.htm'
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
