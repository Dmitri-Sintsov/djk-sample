from django.shortcuts import render
from django_jinja_knockout.views import InlineCreateView, KoGridWidget
from .models import Manufacturer
from .forms import ManufacturerForm, ClubFormWithInlineFormsets


def main_page(request):
    if request.method == 'GET':
        return render(request, 'main.htm')


class ClubCreate(InlineCreateView):

    client_routes = [
        'manufacturer_fk_widget_grid'
    ]
    template_name = 'club_create.htm'
    form_with_inline_formsets = ClubFormWithInlineFormsets


class ManufacturerFkWidgetGrid(KoGridWidget):

    model = Manufacturer
    form = ManufacturerForm

    grid_fields = '__all__'

    def get_actions(self):
        actions = super().get_actions()
        actions['glyphicon']['delete']['enabled'] = True
        actions['built_in']['delete_confirmed']['enabled'] = True
        return actions
