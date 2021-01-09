from django.shortcuts import render
from django_jinja_knockout import tpl
from django_jinja_knockout.viewmodels import vm_list
from django_jinja_knockout.views import create_page_context, ModelFormActionsView

from .forms import UserPreferencesForm


def renderer_test(request, **kwargs):
    renderer_child = tpl.Renderer(request, template='child.htm', context={
        'd': 4,
    })
    renderer_top = tpl.Renderer(request, template='top.htm', context={
        'a': 1,
        'b': 2,
        'child': renderer_child,
        'c': 3,
    })
    return render(request, 'renderer_test.htm', {
        # Test template_context without decorator.
        'page_context': create_page_context(request),
        'renderer_top': renderer_top
    })


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
