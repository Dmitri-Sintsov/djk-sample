from django_jinja_knockout.automation import AutomationCommands
from django_jinja_knockout.testing import DjkSeleniumCommands

for command in DjkSeleniumCommands.yield_command_names():
    globals()[command] = command


class SportClub(AutomationCommands):

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
                ('id_title', self._.club['title']),
                ('id_foundation_date', self._.club['foundation_date']),
                'input_as_select_click', ('id_category_1',),
            )


class SportClubInventory(AutomationCommands):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_idx = kwargs.pop('formset_idx')

    def new_formset_form(self):
        yield relative_form_button_click, ('Add "Sport club equipment"',),

    def add_manufacturers(self):
        for key, manufacturer in enumerate(self._.manufacturers):
            is_last_key = key + 1 == len(self._.manufacturers)
            yield from self.add_manufacturer(manufacturer, is_last_key)

    def add_manufacturer(self, manufacturer, is_last_manufacturer):
        select_commands = (
            grid_find_data_row, ({'Company name': manufacturer['company_name']},),
        )
        if manufacturer['_create_']:
            add_commands = (
                dialog_button_click, ('Save',),
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
                    'id_equipment_set-{}-manufacturer'.format(self.formset_idx),
                    add_commands,
                    select_commands
                ),
                wait_until_dialog_closes,
            )
        else:
            yield (
                fk_widget_click, ('id_equipment_set-{}-manufacturer'.format(self.formset_idx),),
            ) + select_commands + (
                grid_select_current_row,
                dialog_button_click, ('Apply',),
                wait_until_dialog_closes,
            )
        for key, inventory in enumerate(manufacturer['inventories']):
            yield from self.add_manufacturer_inventory(inventory)
            self.formset_idx += 1
            if not is_last_manufacturer or key + 1 < len(manufacturer['inventories']):
                yield from self.new_formset_form()
                yield (
                    fk_widget_click, ('id_equipment_set-{}-manufacturer'.format(self.formset_idx),),
                )
                yield select_commands
                yield (
                    grid_select_current_row,
                    dialog_button_click, ('Apply',),
                )

    def add_manufacturer_inventory(self, inventory):
        yield (
            keys_by_id, (
                'id_equipment_set-{}-inventory_name'.format(self.formset_idx), inventory['name']
            ),
            input_as_select_click, (
                'id_equipment_set-{}-category_{}'.format(self.formset_idx, inventory['category_id']),
            ),
        )

    def test_formset_removal(self):
        yield from self.new_formset_form()
        yield (
            by_id, (
                'id_equipment_set-{}-DELETE'.format(self.formset_idx),
            ),
            click,
            to_top_bootstrap_dialog,
            dialog_button_click, ('Yes',),
            wait_until_dialog_closes,
            form_by_view, self._.form_view,
        )


class SportClubMembers(AutomationCommands):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_idx = kwargs.pop('formset_idx')

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
                    'id_member_set-{}-profile'.format(self.formset_idx),
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
                fk_widget_click, ('id_member_set-{}-profile'.format(self.formset_idx),),
            ) + select_commands + (
                grid_select_current_row,
                dialog_button_click, ('Apply',),
                wait_until_dialog_closes,
            )
        yield (
            keys_by_id,
            ('id_member_set-{}-last_visit'.format(self.formset_idx), member['last_visit']),
            ('id_member_set-{}-note'.format(self.formset_idx), member['note']),
            input_as_select_click, (
                'id_member_set-{}-plays_{}'.format(self.formset_idx, member['plays']),
            ),
            input_as_select_click, (
                'id_member_set-{}-role_{}'.format(self.formset_idx, member['role']),
            ),
        )
        if member['is_endorsed']:
            yield (
                by_id, ('id_member_set-{}-is_endorsed'.format(self.formset_idx),),
                click,
            )
