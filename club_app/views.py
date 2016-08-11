from collections import OrderedDict
from django.shortcuts import render
from django_jinja_knockout.views import InlineCreateView, KoGridWidget
from .models import Manufacturer, Profile
from .forms import ManufacturerForm, ProfileForm, ClubFormWithInlineFormsets


def main_page(request):
    if request.method == 'GET':
        return render(request, 'main.htm')


class ClubCreate(InlineCreateView):

    client_routes = [
        'manufacturer_fk_widget_grid',
        'profile_fk_widget_grid'
    ]
    template_name = 'club_create.htm'
    form_with_inline_formsets = ClubFormWithInlineFormsets


class ManufacturerFkWidgetGrid(KoGridWidget):

    model = Manufacturer
    form = ManufacturerForm
    enable_deletion = True
    grid_fields = '__all__'
    allowed_sort_orders = '__all__'
    allowed_filter_fields = OrderedDict([
        ('direct_shipping', None)
    ])


class ProfileFkWidgetGrid(KoGridWidget):

    model = Profile
    form = ProfileForm
    enable_deletion = True
    grid_fields = ['first_name', 'last_name']
    allowed_sort_orders = '__all__'
