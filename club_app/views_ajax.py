from collections import OrderedDict
from copy import copy
import json

from django.utils import timezone
from django.utils.translation import gettext as _
from django.template.defaultfilters import pluralize
from django.db.models import Count

from django_jinja_knockout.query import FilteredRawQuerySet
from django_jinja_knockout.views import KoGridView, KoGridInline, FormatTitleMixin, ContextDataMixin
from django_jinja_knockout.viewmodels import vm_list
from django_jinja_knockout.utils.sdv import get_choice_str, nested_update

from .models import Club, Manufacturer, Profile, Member, Equipment
from .forms import (
    ClubForm, ClubFormWithInlineFormsets,
    ManufacturerForm, ProfileForm, ClubEquipmentForm, MemberForm
)


class SimpleClubGrid(KoGridView):

    model = Club
    grid_fields = '__all__'
    # Remove next line to disable columns sorting:
    allowed_sort_orders = '__all__'


class SimpleClubGridDTL(ContextDataMixin, SimpleClubGrid):
    template_name = 'club_grid.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['club_grid_options'] = {
            'pageRoute': self.request.url_name
        }
        return context_data


class EditableClubGrid(KoGridInline, SimpleClubGrid):

    search_fields = [
        ('title', 'icontains')
    ]
    client_routes = {
        'manufacturer_fk_widget_grid',
        'profile_fk_widget_grid'
    }
    enable_deletion = True
    form_with_inline_formsets = ClubFormWithInlineFormsets


class ClubGridRawQuery(SimpleClubGrid):

    template_name = 'cbv_grid_breadcrumbs.htm'
    grid_fields = [
        'first_name',
        'last_name',
        'role',
        'title',
        'category',
        'foundation_date',
    ]

    allowed_filter_fields = OrderedDict([
        ('category', None),
        ('foundation_date', None),
        ('role', None)
    ])

    def get_model_meta(self, key):
        if key == 'verbose_name_plural':
            # Override grid title.
            return 'Sport clubs and their members'
        else:
            return super().get_model_meta(key)

    def get_field_verbose_name(self, field_name):
        if field_name == 'first_name':
            return 'First name'
        elif field_name == 'last_name':
            return 'Last name'
        elif field_name == 'role':
            return 'Role'
        else:
            return super().get_field_verbose_name(field_name)

    def get_field_validator(self, fieldname):
        if fieldname == 'role':
            return self.__class__.field_validator(self, fieldname, model_class=Member)
        else:
            return super().get_field_validator(fieldname)

    def get_row_str_fields(self, obj, row=None):
        str_fields = super().get_row_str_fields(obj, row)
        if str_fields is None:
            str_fields = {}
        # Add formatted display of manually JOINed field.
        str_fields['role'] = get_choice_str(Member.ROLES, row['role'])
        return str_fields

    def get_base_queryset(self):
        # Mostly supposed to work with LEFT JOIN. Might produce wrong results with arbitrary queries.
        raw_qs = self.model.objects.raw(
            'SELECT club_app_club.*, club_app_member.role, '
            'club_app_profile.first_name, club_app_profile.last_name FROM club_app_club '
            'LEFT JOIN club_app_member ON club_app_club.id = club_app_member.club_id '
            'LEFT JOIN club_app_profile ON club_app_profile.id = club_app_member.profile_id '
        )
        fqs = FilteredRawQuerySet.clone_raw_queryset(
            raw_qs=raw_qs, relation_map={
                'role': 'member',
                'first_name': 'member__profile',
                'last_name': 'member__profile'
            }
        )
        return fqs


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

    def get_model_fields(self):
        model_fields = copy(super().get_model_fields())
        # Remove annotated field which is unavailable when creating / updating single object which does not use
        # self.get_base_queryset()
        # Required only because current grid is editable.
        model_fields.remove('total_members')
        return model_fields

    def postprocess_row(self, row, obj):
        # Add virtual field value.
        row['exists_days'] = (timezone.now().date() - obj.foundation_date).days
        if 'total_members' not in row:
            # Add annotated field value which is unavailable when creating / updating single object which does not use
            # self.get_base_queryset()
            # Required only because current grid is editable.
            row['total_members'] = obj.member_set.count()
        row = super().postprocess_row(row, obj)
        return row

    # Optional formatting of virtual field (not required).
    def get_row_str_fields(self, obj, row=None):
        str_fields = super().get_row_str_fields(obj, row)
        if str_fields is None:
            str_fields = {}
        # Add formatted display of virtual field.
        is_plural = pluralize(row['exists_days'], arg='days')
        str_fields['exists_days'] = '{} {}'.format(row['exists_days'], 'day' if is_plural == '' else is_plural)
        return str_fields


class ClubGridWithActionLogging(ClubGridWithVirtualField, EditableClubGrid):

    template_name = 'club_grid_with_action_logging.htm'
    client_routes = {
        'user_fk_widget_grid',
        'manufacturer_fk_widget_grid',
        'profile_fk_widget_grid',
        'action_grid',
    }
    grid_options = {
        # Note: 'classPath' is not required for standard App.ko.Grid.
        'classPath': 'App.ko.ClubGrid',
    }


class ClubEquipmentGrid(EditableClubGrid):

    client_routes = {
        # Injected in djk_sample.context_processors.TemplateContextProcessor.CLIENT_ROUTES,
        # just for the test of global route injection.
        # 'equipment_grid',
        'club_grid_simple',
        'manufacturer_fk_widget_grid',
    }
    template_name = 'club_equipment.htm'
    form = ClubForm
    form_with_inline_formsets = None

    def get_actions(self):
        actions = super().get_actions()
        actions['built_in']['save_equipment'] = {}
        actions['glyphicon']['add_equipment'] = {
            'localName': _('Add club equipment'),
            'css': 'glyphicon-wrench',
        }
        return actions

    # Creates AJAX ClubEquipmentForm bound to particular Club instance.
    def action_add_equipment(self):
        club = self.get_object_for_action()
        if club is None:
            return vm_list({
                'view': 'alert_error',
                'title': 'Error',
                'message': 'Unknown instance of Club'
            })
        equipment_form = ClubEquipmentForm(initial={'club': club.pk})
        # Generate equipment_form viewmodel
        vms = self.vm_form(
            equipment_form, form_action='save_equipment'
        )
        return vms

    # Validates and saves the Equipment model instance via bound ClubEquipmentForm.
    def action_save_equipment(self):
        form = ClubEquipmentForm(self.request.POST)
        if not form.is_valid():
            form_vms = vm_list()
            self.add_form_viewmodels(form, form_vms)
            return form_vms
        equipment = form.save()
        club = equipment.club
        club.last_update = timezone.now()
        club.save()
        # Instantiate related EquipmentGrid to use it's .postprocess_qs() method
        # to update it's row via grid viewmodel 'prepend_rows' key value.
        equipment_grid = EquipmentGrid()
        equipment_grid.request = self.request
        equipment_grid.init_class()
        return vm_list({
            'update_rows': self.postprocess_qs([club]),
            # return grid rows for client-side EquipmentGrid component .updatePage(),
            'equipment_grid_view': {
                'prepend_rows': equipment_grid.postprocess_qs([equipment])
            }
        })


class EquipmentGrid(KoGridView):
    model = Equipment
    form = ClubEquipmentForm
    enable_deletion = True
    grid_fields = [
        'club',
        'manufacturer__company_name',
        'manufacturer__direct_shipping',
        'inventory_name',
        'category',
    ]
    search_fields = [
        ('inventory_name', 'icontains')
    ]
    allowed_sort_orders = [
        'manufacturer__company_name',
        'inventory_name',
        'category'
    ]
    allowed_filter_fields = OrderedDict([
        ('club', {
            'pageRoute': 'club_grid_simple',
            # Optional setting for BootstrapDialog:
            'dialogOptions': {'size': 'size-wide'},
        }),
        ('manufacturer', {
            'pageRoute': 'manufacturer_fk_widget_grid'
        }),
        ('manufacturer__direct_shipping', None),
        ('category', None)
    ])
    grid_options = {
        'searchPlaceholder': 'Search inventory name',
    }

    def get_actions(self):
        # Disable adding new Equipment because ClubEquipmentForm is incomplete (has no Club) for action 'create_form'.
        # ClubEquipmentGrid.action_add_equipment is used instead.
        actions = super().get_actions()
        actions['button']['create_form']['enabled'] = False
        return actions


class MemberGrid(KoGridView):

    client_routes = {
        'member_grid',
        'profile_fk_widget_grid',
        'club_grid_simple'
    }
    template_name = 'member_grid.htm'
    model = Member
    grid_fields = [
        'profile',
        'club',
        # Compound columns:
        [
            # Will join 'category' field from related 'Club' table automatically via Django ORM.
            'club__category',
            'last_visit',
            'plays',
            'role',
        ],
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
        # Include only some Django model field choices and disable multiple choices for 'plays' filter.
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
    def get_grid_options(cls):
        return {
            # Note: 'classPath' is not required for standard App.ko.Grid.
            'classPath': 'App.ko.MemberGrid',
            'searchPlaceholder': 'Search for club or member profile',
            'fkGridOptions': {
                'profile': {
                    'pageRoute': 'profile_fk_widget_grid'
                },
                'club': {
                    'pageRoute': 'club_grid_simple',
                    # Optional setting for BootstrapDialog:
                    'dialogOptions': {'size': 'size-wide'},
                }
            }
        }

    # Overriding get_base_queryset() is not required, but is used to reduce number of queries.
    def get_base_queryset(self):
        return self.__class__.model.objects.select_related('club').all()


class ClubMemberGrid(FormatTitleMixin, MemberGrid):

    format_view_title = True
    grid_fields = [
        'profile',
        [
            'plays',
            'role',
        ],
        [
            'last_visit',
            'is_endorsed'
        ],
        'note',
    ]
    allowed_filter_fields = OrderedDict([
        ('profile', None),
        ('last_visit', None),
        ('plays', None),
        ('role', None),
        ('is_endorsed', None),
    ])

    def get_base_queryset(self):
        return super().get_base_queryset().filter(club_id=self.kwargs['club_id'])

    def get(self, request, *args, **kwargs):
        club = Club.objects.filter(pk=self.kwargs['club_id']).first()
        if club is not None:
            self.format_title(club)
        return super().get(request, *args, **kwargs)


class MemberGridTabs(MemberGrid):

    template_name = 'member_grid_tabs.htm'
    enable_deletion = True

    allowed_filter_fields = OrderedDict([
        ('profile', None),
        ('last_visit', None),
        # Next choices of 'plays' field filter will be set when grid loads.
        ('plays', {'active_choices': [Member.SPORT_BADMINTON, Member.SPORT_SQUASH]}),
        ('role', None),
        ('is_endorsed', None),
    ])

    @classmethod
    def get_grid_options(cls):
        grid_options = super().get_grid_options()
        grid_options['highlightMode'] = 'cycleColumns'
        return grid_options

    # Do not allow to delete Member instances with role=Member.ROLE_FOUNDER:
    def action_delete_is_allowed(self, objects):
        # ._clone() is required because original pagination queryset is passed as objects argument.
        qs = objects._clone()
        return not qs.filter(role=Member.ROLE_FOUNDER).exists()


class MemberGridCustomActions(MemberGrid):

    template_name = 'member_grid_custom_actions.htm'
    form = MemberForm

    def get_actions(self):
        actions = super().get_actions()
        nested_update(actions, {
            'built_in': {
                'endorse_members': {},
            },
            'click': {
                'edit_note': {
                    'localName': _('Edit member note'),
                    'css': 'btn-warning',
                },
            },
            'glyphicon': {
                'quick_endorse': {
                    'localName': _('Quick endorsement'),
                    'css': 'glyphicon-cloud-upload',
                },
                'quick_disendorse': {
                    'localName': _('Quick disendorsement'),
                    'css': 'glyphicon-cloud-download',
                }
            }
        })
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
            'description': [list(member.get_str_fields().values()) for member in modified_members],
            'update_rows': self.postprocess_qs(modified_members),
        })

    def change_endorsement(self, is_endorsed):
        member = self.get_object_for_action()
        modified_members = []
        if member.is_endorsed != is_endorsed:
            member.is_endorsed = is_endorsed
            member.save()
            modified_members.append(member)
        return vm_list({
            'update_rows': self.postprocess_qs(modified_members),
        })

    def action_quick_endorse(self):
        return self.change_endorsement(is_endorsed=True)

    def action_quick_disendorse(self):
        return self.change_endorsement(is_endorsed=False)

    def action_edit_note(self):
        member = self.get_object_for_action()
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
                'update_rows': self.postprocess_qs(modified_members),
            })


class ManufacturerFkWidgetGrid(KoGridView):

    model = Manufacturer
    form = ManufacturerForm
    enable_deletion = True
    grid_fields = '__all__'
    allowed_sort_orders = '__all__'
    allowed_filter_fields = OrderedDict([
        ('direct_shipping', None)
    ])
    search_fields = [
        ('company_name', 'icontains'),
    ]


class ProfileFkWidgetGrid(KoGridView):

    model = Profile
    form = ProfileForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = ['first_name', 'last_name']
    allowed_sort_orders = '__all__'
    search_fields = [
        ('first_name', 'icontains'),
        ('last_name', 'icontains'),
    ]
