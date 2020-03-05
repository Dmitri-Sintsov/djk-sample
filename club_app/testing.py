from django_jinja_knockout.automation import AutomationCommands
from django_jinja_knockout.testing import DjkSeleniumCommands

for command in DjkSeleniumCommands.yield_command_names():
    globals()[command] = command


class FormPrefixMixin:

    def __init__(self, *args, **kwargs):
        self.prefix = kwargs.get('prefix', '')
        if self.prefix != '':
            self.prefix += '-'


class SportClub(FormPrefixMixin, AutomationCommands):

    def club_form_view(self):
        yield (
            click_anchor_by_view, self._.form_view,
            # Next one step is optional:
            form_by_view, self._.form_view,
        )

    def club_base_info(self):
        if hasattr(self._, 'club'):
            yield (
                keys_by_id,
                ('id_{}title'.format(self.prefix), self._.club['title']),
                ('id_{}foundation_date'.format(self.prefix), self._.club['foundation_date']),
                'input_as_select_click', ('id_{}category_{}'.format(self.prefix, self._.club['category_id']),),
            )


class SportClubInventory(FormPrefixMixin, AutomationCommands):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set to None to automate single manufacturer equipment form.
        # Set to number to add one or multiple manufacturer equipment inline formsets.
        self.formset_idx = kwargs['formset_idx']

    def new_formset_form(self):
        yield relative_form_button_click, ('Add "Sport club equipment"',),

    def add_club_tag(self, club_tag_name):
        yield (
            fk_widget_add_and_select, {
                'fk_id': 'id_{}tag_set'.format(self.prefix),
                'add_commands': (
                    keys_by_id, ('id_name', club_tag_name),
                ),
                'select_commands': (
                    grid_find_data_row, ({'Tag': club_tag_name},),
                )
            },
        )

    def remove_club_tag(self, club_tag_name):
        yield (
            'fk_widget_remove_value', (
                'id_{}tag_set'.format(self.prefix),
                club_tag_name,
            ),
        )

    def add_club_tags(self):
        for club_tag_name in ['Russia', 'Moscow', 'Yaroslavl']:
            yield from self.add_club_tag(club_tag_name)

    def remove_club_tags(self):
        for club_tag_name in ['Moscow']:
            yield from self.remove_club_tag(club_tag_name)

    def add_manufacturers(self):
        for key, manufacturer in enumerate(self._.manufacturers):
            is_last_key = key + 1 == len(self._.manufacturers)
            yield from self.add_manufacturer(manufacturer, is_last_key)

    def get_id_for_field(self, fieldname):
        if self.formset_idx is None:
            return 'id_{}{}'.format(self.prefix, fieldname)
        else:
            return 'id_{}equipment_set-{}-{}'.format(self.prefix, self.formset_idx, fieldname)

    def add_manufacturer(self, manufacturer, is_last_manufacturer):
        select_commands = (
            grid_find_data_row, ({'Company name': manufacturer['company_name']},),
        )
        if manufacturer['_create_']:
            add_commands = (
                dialog_footer_button_click, ('Save',),
                assert_field_error, ('id_company_name', 'This field is required.'),
                keys_by_id, ('id_company_name', manufacturer['company_name']),
            )
            if manufacturer['direct_shipping']:
                add_commands += (
                    by_id, ('id_direct_shipping',),
                    click,
                )
            yield (
                fk_widget_add_and_select, (
                    self.get_id_for_field('manufacturer'),
                    add_commands,
                    select_commands
                ),
                wait_until_dialog_closes,
            )
        else:
            yield (
                fk_widget_click, (self.get_id_for_field('manufacturer'),),
            ) + select_commands + (
                grid_select_current_row,
                dialog_footer_button_click, ('Apply',),
                wait_until_dialog_closes,
            )
        for key, inventory in enumerate(manufacturer['inventories']):
            yield from self.add_manufacturer_inventory(inventory)
            if self.formset_idx is None:
                if len(manufacturer['inventories']) > 1:
                    raise ValueError('Single form cannot have multiple inventories')
                break
            self.formset_idx += 1
            if not is_last_manufacturer or key + 1 < len(manufacturer['inventories']):
                yield from self.new_formset_form()
                yield (
                    fk_widget_click, (self.get_id_for_field('manufacturer'),),
                )
                yield select_commands
                yield (
                    grid_select_current_row,
                    dialog_footer_button_click, ('Apply',),
                )

    def add_manufacturer_inventory(self, inventory):
        yield (
            keys_by_id, (
                self.get_id_for_field('inventory_name'), inventory['name']
            ),
            input_as_select_click, (
                (self.get_id_for_field('category') + '_{}').format(inventory['category_id']),
            ),
        )

    def test_formset_removal(self):
        yield from self.new_formset_form()
        yield (
            by_id, (
                self.get_id_for_field('DELETE'),
            ),
            click,
            to_top_bootstrap_dialog,
            dialog_footer_button_click, ('Yes',),
            wait_until_dialog_closes,
            form_by_view, self._.form_view,
        )


class SportClubMembers(FormPrefixMixin, AutomationCommands):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_idx = kwargs['formset_idx']

    def new_formset_form(self):
        yield 'relative_form_button_click', ('Add "Sport club member"',),

    def add_members(self):
        for key, member in enumerate(self._.members):
            is_last_member = key + 1 == len(self._.members)
            yield from self.add_member(member, is_last_member)
            self.formset_idx += 1

    def add_member(self, member, is_last_member):
        yield from self.new_formset_form()
        select_commands = (
            grid_find_data_row, ({'First name': member['first_name']},),
        )
        if member['_create_profile_']:
            yield (
                fk_widget_add_and_select, (
                    'id_{}member_set-{}-profile'.format(self.prefix, self.formset_idx),
                    (
                        keys_by_id,
                        ('id_first_name', member['first_name']),
                        ('id_last_name', member['last_name']),
                        ('id_birth_date', member['birth_date']),
                    ),
                    select_commands,
                ),
                wait_until_dialog_closes,
            )
        else:
            yield (
                fk_widget_click, ('id_{}member_set-{}-profile'.format(self.prefix, self.formset_idx),),
            ) + select_commands + (
                grid_select_current_row,
                dialog_footer_button_click, ('Apply',),
                wait_until_dialog_closes,
            )
        yield (
            keys_by_id,
            ('id_{}member_set-{}-last_visit'.format(self.prefix, self.formset_idx), member['last_visit']),
            ('id_{}member_set-{}-note'.format(self.prefix, self.formset_idx), member['note']),
            input_as_select_click, (
                'id_{}member_set-{}-plays_{}'.format(self.prefix, self.formset_idx, member['plays']),
            ),
            input_as_select_click, (
                'id_{}member_set-{}-role_{}'.format(self.prefix, self.formset_idx, member['role']),
            ),
        )
        if member['is_endorsed']:
            yield (
                by_id, ('id_{}member_set-{}-is_endorsed'.format(self.prefix, self.formset_idx),),
                click,
            )
