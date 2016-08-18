from collections import OrderedDict
from django_jinja_knockout.views import KoGridView, KoGridWidget
from .models import Club, Equipment, Manufacturer, Profile, Member
from .forms import ManufacturerForm, ProfileForm


class SimpleClubGrid(KoGridView):

    client_routes = [
        'club_grid_simple'
    ]
    template_name = 'club_grid_simple.htm'
    model = Club
    grid_fields = '__all__'
    # Remove next line to disable columns sorting:
    allowed_sort_orders = '__all__'


class MemberGrid(KoGridView):

    client_routes = [
        'member_grid',
        'profile_fk_widget_grid',
        'club_grid_simple'
    ]
    template_name = 'member_grid.htm'
    model = Member
    grid_fields = [
        'profile',
        'club',
        # Will join 'category' field from related 'Club' table automatically via Django ORM.
        'club__category',
        'last_visit',
        'plays',
        'role',
        'note',
        'is_endorsed'
    ]
    allowed_sort_orders = [
        'club',
        # Will join 'category' field from related 'Club' table automatically via Django ORM.
        # 'club__category',
        'last_visit',
        'plays',
        'is_endorsed'
    ]
    allowed_filter_fields = OrderedDict([
        ('profile', None),
        ('club', None),
        ('club__category', None),
        ('last_visit', None),
        # Include only some Django model choices and disable multiple choices for 'plays' filter.
        ('plays', {
            'type': 'choices', 'choices': Member.BASIC_SPORTS, 'multiple_choices': False
        }),
        ('role', None),
        ('is_endorsed', None),
    ])

    def get_field_verbose_name(self, field_name):
        if field_name == 'club__category':
            return 'Club category'
        else:
            return super().get_field_verbose_name(field_name)

    @classmethod
    def get_default_grid_options(cls):
        return {
            'fkGridOptions': {
                'profile': {
                    'pageRoute': 'profile_fk_widget_grid'
                },
                'club': {
                    'pageRoute': 'club_grid_simple'
                }
            }
        }


class EquipmentGrid(KoGridView):

    client_routes = [
        'equipment_grid'
    ]
    template_name = 'equipment_grid.htm'
    model = Equipment
    grid_fields = [
        'manufacturer',
        # Will join 'direct_shipping' field from related 'Manufacturer' table automatically via Django ORM.
        'manufacturer__direct_shipping',
        'inventory_name',
        # Will join 'title' field from related 'Club' table automatically via Django ORM.
        'club__category',
        'category',
    ]
    allowed_sort_orders = '__all__'
    allowed_filter_fields = OrderedDict([
        ('manufacturer', None),
        ('club_category', None),
        ('category', {
            'type': 'choices', 'choices': Equipment.CATEGORIES, 'multiple_choices': False
        }),
    ])


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
