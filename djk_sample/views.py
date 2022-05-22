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
        'renderer_top': renderer_top
    })


def tooltips_test(request, **kwargs):
    page_context = create_page_context(request)
    page_context.set_custom_scripts(
        'sample/js/tooltips-test.js',
    )
    # Test template_context without decorator.
    return render(request, 'tooltips_test.htm', {
        'page_context': page_context,
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
