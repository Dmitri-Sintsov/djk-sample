from collections import OrderedDict
from django_jinja_knockout.views import KoGridView, KoGridWidget
from .models import Club, Equipment, Manufacturer, Profile, Member
from .forms import ManufacturerForm, ProfileForm


class SimpleClubGrid(KoGridView):

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
    search_fields = [
        ('club__title', 'icontains'),
        ('profile__first_name', 'icontains'),
        ('profile__last_name', 'icontains')
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
        ('last_visit', None),
        ('club__category', None),
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
            # Note: 'classPath' is not required for standard App.ko.Grid.
            'classPath': 'App.ko.MemberGrid',
            'fkGridOptions': {
                'profile': {
                    'pageRoute': 'profile_fk_widget_grid'
                },
                'club': {
                    'pageRoute': 'club_grid_simple'
                }
            }
        }

    # Overriding get_base_queryset() is not required, but is used to reduce number of queries.
    def get_base_queryset(self):
        return self.__class__.model.objects.select_related('club').all()

class MemberGridTabs(MemberGrid):

    template_name = 'member_grid_tabs.htm'


class ClubGridWithVirtualField(SimpleClubGrid):

    grid_fields = [
        'title', 'category', 'foundation_date', 'total_members'
    ]

    def get_field_verbose_name(self, field_name):
        if field_name == 'total_members':
            # Add virtual field.
            return 'Total members'
        else:
            return super().get_field_verbose_name(field_name)

    def get_related_fields(self, query_fields=None):
        query_fields = super().get_related_fields(query_fields)
        # Remove virtual field from queryset values().
        query_fields.remove('total_members')
        return query_fields

    def postprocess_row(self, row, obj):
        # Add virtual field value.
        row['total_members'] = obj.member_set.count()
        row = super().postprocess_row(row, obj)
        return row

    # Optional formatting of virtual field (not required).
    def get_row_str_fields(self, obj, row):
        str_fields = super().get_row_str_fields(obj, row)
        if str_fields is None:
            str_fields = {}
        # Add formatted display of virtual field.
        str_fields['total_members'] = 'None yet' if row['total_members'] == 0 else row['total_members']
        return str_fields


# Currently is unused.
class EquipmentGrid(KoGridView):

    client_routes = [
        'equipment_grid'
    ]
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
