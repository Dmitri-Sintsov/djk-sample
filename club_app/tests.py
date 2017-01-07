from django_jinja_knockout.viewmodels import to_json
from django_jinja_knockout.automation import AutomationCommands


class SportClub(AutomationCommands):

    def club_base_info(self):
        yield (
            'click_anchor_by_view', self._.form_view,
            # Next one step is optional:
            'form_by_view', self._.form_view,
        )
        if hasattr(self._, 'club'):
            yield (
                'keys_by_id',
                ('id_title', self._.club['title']),
                ('id_foundation_date', self._.club['foundation_date']),
                'input_as_select_click', ('id_category_1',),
            )


class SportClubInventory(AutomationCommands):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_idx = kwargs.pop('formset_idx')

    def new_formset_form(self):
        yield 'relative_form_button_click', ('Add "Sport club equipment"',),

    def add_manufacturers(self):
        for key, manufacturer in enumerate(self._.manufacturers):
            is_last_key = key + 1 == len(self._.manufacturers)
            yield from self.add_manufacturer(manufacturer, is_last_key)

    def add_manufacturer(self, manufacturer, is_last_manufacturer):
        add_commands = (
            'dialog_button_click', ('Save',),
            'assert_field_error', ('id_company_name', 'This field is required.'),
            'keys_by_id', ('id_company_name', manufacturer['company_name']),
        )
        if manufacturer['direct_shipping']:
            add_commands += (
                'by_id', ('id_direct_shipping',),
                'click',
            )
        select_commands = (
            'grid_find_data_column', ('Company name', manufacturer['company_name']),
        )
        yield (
            'fk_widget_add_and_select', (
                'id_equipment_set-{}-manufacturer'.format(self.formset_idx),
                add_commands,
                select_commands
            ),
        )
        for key, inventory in enumerate(manufacturer['inventories']):
            yield from self.add_manufacturer_inventory(inventory)
            self.formset_idx += 1
            if not is_last_manufacturer or key + 1 < len(manufacturer['inventories']):
                yield from self.new_formset_form()
                yield (
                    'fk_widget_click', ('id_equipment_set-{}-manufacturer'.format(self.formset_idx),),
                )
                yield select_commands
                yield (
                    'grid_select_current_row',
                    'dialog_button_click', ('Apply',),
                )

    def add_manufacturer_inventory(self, inventory):
        yield (
            'keys_by_id', (
                'id_equipment_set-{}-inventory_name'.format(self.formset_idx), inventory['name']
            ),
            'input_as_select_click', (
                'id_equipment_set-{}-category_{}'.format(self.formset_idx, inventory['category_id']),
            ),
        )

    def test_formset_removal(self):
        yield from self.new_formset_form()
        yield (
            'by_id', (
                'id_equipment_set-{}-DELETE'.format(self.formset_idx),
            ),
            'click',
            'to_top_bootstrap_dialog',
            'dialog_button_click', ('Yes',),
            'form_by_view', self._.form_view,
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
        yield (
            'fk_widget_add_and_select', (
                'id_member_set-{}-profile'.format(self.formset_idx),
                (
                    'keys_by_id',
                    ('id_first_name', member['first_name']),
                    ('id_last_name', member['last_name']),
                    ('id_birth_date', member['birth_date']),
                ),
                (
                    'grid_find_data_column', ('First name', member['first_name']),
                )
            ),
            'keys_by_id',
            ('id_member_set-{}-last_visit'.format(self.formset_idx), member['last_visit']),
            ('id_member_set-{}-note'.format(self.formset_idx), member['note']),
            'input_as_select_click', (
                'id_member_set-{}-plays_{}'.format(self.formset_idx, member['plays']),
            ),
            'input_as_select_click', (
                'id_member_set-{}-role_{}'.format(self.formset_idx, member['role']),
            ),
        )
        if member['is_endorsed']:
            yield (
                'by_id', ('id_member_set-{}-is_endorsed'.format(self.formset_idx),),
                'click',
            )


class UpdateSportClub(AutomationCommands):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.club_id = kwargs.pop('club_id')
        self.update_view = {'viewname': 'club_update', 'kwargs': {'club_id': self.club_id}}

    def open_update_form(self):
        return (
            'click_anchor_by_view', self.update_view,
            'form_by_view', self.update_view,
        )


class ClubAppCommands(AutomationCommands):

    empty_club_list = (
        'click_anchor_by_view', {'viewname': 'club_list'},
        'jumbotron_text', ('There is no',),
        'click_anchor_by_view', (
            'club_list',
            {},
            {
                'list_filter': to_json({
                    'category': 1
                })
            }
        ),
        'jumbotron_text', ('There is no',),
        'reverse_url', (
            'club_list',
            {},
            {
                'list_filter': to_json({
                    'category1': 1
                })
            }
        ),
        'jumbotron_text', ('Not allowed filter field',),
    )

    def add_sport_club(self):
        form_view = ('club_create',)
        yield from SportClub().set_context({
            'form_view': form_view,
            'club': {
                'title': 'Yaroslavl Bears',
                'foundation_date': '1971-08-29',
            },
        }).club_base_info()
        yield from SportClubInventory(formset_idx=0).set_context({
            'manufacturers': [
                {
                    'company_name': 'Yanix',
                    'direct_shipping': True,
                    'inventories': [
                        {
                            'name': 'Silent Air 2020',
                            'category_id': 2,
                        },
                        {
                            'name': 'Frosty Ball 2030',
                            'category_id': 1,
                        },
                    ]
                },
                {
                    'company_name': 'Oldidos',
                    'direct_shipping': False,
                    'inventories': [
                        {
                            'name': 'Nanostrength 5',
                            'category_id': 0,
                        },
                    ]
                }
            ]
        }).add_manufacturers()
        yield from SportClubMembers(
            formset_idx=0
        ).set_context({
            'members': [
                {
                    'first_name': 'Ivan',
                    'last_name': 'Petrov',
                    'birth_date': '1971-07-29',
                    'last_visit': '2016-11-23 14:47:33',
                    'note': 'Veteran of Russian badminton',
                    'plays': 0,
                    'role': 1,
                    'is_endorsed': True,
                },
                {
                    'first_name': 'Liu',
                    'last_name': 'Zhuang',
                    'birth_date': '1982-05-18',
                    'last_visit': '2015-07-15 11:25:17',
                    'note': 'Chinese player with ultra-fast reaction and speed',
                    'plays': 3,
                    'role': 2,
                    'is_endorsed': False,
                }
            ]
        }).add_members()
        yield ('click_submit_by_view', form_view)

    def details_sport_club(self):
        yield (
            'button_click', ('Read',),
            'dialog_button_click', ('OK',),
        )

    def update_sport_club(self):
        form_view = {'viewname': 'club_update', 'kwargs': {'club_id': 1}}
        yield from SportClub().set_context({
            'form_view': form_view,
        }).club_base_info()
        yield from SportClubInventory(formset_idx=3).set_context({
            'form_view': form_view,
            'manufacturers': [
                {
                    'company_name': 'Bubblelat',
                    'direct_shipping': True,
                    'inventories': [
                        {
                            'name': 'Bubble Pro 2010',
                            'category_id': 1,
                        },
                    ]
                },
            ]
        }).yield_class_commands(
            'test_formset_removal',
            'new_formset_form',
            'add_manufacturers',
        )
        yield from SportClubMembers(
            formset_idx=2
        ).set_context({
            'members': [
                {
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'birth_date': '1973-05-19',
                    'last_visit': '2016-11-27 19:27:41',
                    'note': 'Entrepreneur and master of squash',
                    'plays': 3,
                    'role': 0,
                    'is_endorsed': False,
                },
            ]
        }).yield_class_commands(
            # 'new_formset_form',
            'add_members'
        )
        yield ('click_submit_by_view', form_view)
