from collections import OrderedDict
import json

from django.utils import timezone
from django.utils.translation import gettext as _
from django.template.defaultfilters import pluralize
from django.db.models import Count

from django_jinja_knockout.views import KoGridView, KoGridWidget, KoGridInline
from django_jinja_knockout.viewmodels import vm_list

from .models import Club, Equipment, Manufacturer, Profile, Member
from .forms import ClubFormWithInlineFormsets, ManufacturerForm, ProfileForm


class SimpleClubGrid(KoGridView):

    model = Club
    grid_fields = '__all__'
    # Remove next line to disable columns sorting:
    allowed_sort_orders = '__all__'


class EditableClubGrid(KoGridInline, SimpleClubGrid):

    search_fields = [
        ('title', 'icontains')
    ]
    client_routes = [
        'manufacturer_fk_widget_grid',
        'profile_fk_widget_grid'
    ]
    enable_deletion = True
    form_with_inline_formsets = ClubFormWithInlineFormsets


class ClubGridWithVirtualField(SimpleClubGrid):

    grid_fields = [
        'title',
        'category',
        'foundation_date',
        'total_members',
        'exists_days'
    ]

    def get_base_queryset(self):
        return super().get_base_queryset().annotate(total_members=Count('member'))

    def get_field_verbose_name(self, field_name):
        if field_name == 'exists_days':
            # Add virtual field.
            return 'Days since foundation'
        elif field_name == 'total_members':
            # Add annotated field.
            return 'Total members'
        else:
            return super().get_field_verbose_name(field_name)

    def get_related_fields(self, query_fields=None):
        query_fields = super().get_related_fields(query_fields)
        # Remove virtual field from queryset values().
        query_fields.remove('exists_days')
        return query_fields

    def postprocess_row(self, row, obj):
        # Add virtual field value.
        row['exists_days'] = (timezone.now().date() - obj.foundation_date).days
        row = super().postprocess_row(row, obj)
        return row

    # Optional formatting of virtual field (not required).
    def get_row_str_fields(self, obj, row):
        str_fields = super().get_row_str_fields(obj, row)
        if str_fields is None:
            str_fields = {}
        # Add formatted display of virtual field.
        is_plural = pluralize(row['exists_days'], arg='days')
        str_fields['exists_days'] = '{} {}'.format(row['exists_days'], 'day' if is_plural == '' else is_plural)
        return str_fields


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
            'searchPlaceholder': 'Search for club or member profile',
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


class MemberGridCustomActions(MemberGrid):

    template_name = 'member_grid_custom_actions.htm'

    def get_actions(self):
        actions = super().get_actions()
        actions['built_in']['endorse_members'] = {'enabled': True}
        # action_type = 'glyphicon'
        action_type = 'click'
        actions[action_type]['edit_note'] = {
            'localName': _('Edit member note'),
            # 'class': 'glyphicon-cloud-upload',
            'class': 'btn-warning',
            'enabled': True
        }
        return actions

    def action_endorse_members(self):
        member_ids = json.loads(self.request_get('member_ids', '{}'))
        if not isinstance(member_ids, dict):
            return vm_list({
                'view': 'alert_error',
                'title': 'Invalid value of member_ids',
                'message': self.request_get('member_ids')
            })
        members = self.model.objects.filter(pk__in=member_ids)
        modified_members = []
        for member in members:
            if member.is_endorsed != member_ids[str(member.pk)]:
                member.is_endorsed = member_ids[str(member.pk)]
                member.save()
                modified_members.append(member)
        return vm_list({
            'view': self.__class__.viewmodel_name,
            'description': [list(member.get_str_fields().values()) for member in modified_members],
            'update_rows': self.postprocess_qs(modified_members),
        })

    def action_edit_note(self):
        member = self.get_object_from_action_template()
        note = self.request_get('note')
        modified_members = []
        if member.note != note:
            member.note = note
            member.save()
            modified_members.append(member)
        if len(modified_members) == 0:
            return vm_list({
                'view': 'alert',
                'title': str(member.profile),
                'message': 'Note was not changed.'
            })
        else:
            return vm_list({
                'view': self.__class__.viewmodel_name,
                'update_rows': self.postprocess_qs(modified_members),
            })


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
