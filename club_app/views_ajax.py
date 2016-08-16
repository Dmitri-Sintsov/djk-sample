from collections import OrderedDict
from django_jinja_knockout.views import KoGridView, KoGridWidget
from .models import Club, Manufacturer, Profile
from .forms import ManufacturerForm, ProfileForm


class SimpleClubGrid(KoGridView):

    client_routes = [
        'club_grid_simple'
    ]
    template_name = 'club_grid_simple.htm'
    model = Club
    grid_fields = '__all__'


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
