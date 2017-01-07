from django_jinja_knockout.viewmodels import to_json
from django_jinja_knockout.automation import AutomationCommands


class AddSportClub(AutomationCommands):

    def club_base_info(self):
        yield (
            'click_anchor_by_view', {'viewname': 'club_create'},
            # Next one step is optional:
            'form_by_view', ('club_create',),
            'keys_by_id',
            ('id_title', self._.club['title']),
            ('id_foundation_date', self._.club['foundation_date']),
            'input_as_select_click', ('id_category_1',),
        )


class AddSportClubInventory(AutomationCommands):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_idx = kwargs.pop('formset_idx')

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
                yield (
                    'relative_form_button_click', ('Add "Sport club equipment"',),
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


class AddSportClubMembers(AutomationCommands):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_idx = kwargs.pop('formset_idx')

    def add_member(self):
        yield (
            'relative_form_button_click', ('Add "Sport club member"',),
            'fk_widget_add_and_select', (
                'id_member_set-0-profile',
                (
                    'keys_by_id',
                    ('id_first_name', 'Ivan',),
                    ('id_last_name', 'Petrov',),
                    ('id_birth_date', '1971-07-29',),
                ),
                (
                    'grid_find_data_column', ('First name', 'Ivan'),
                )
            ),
            'keys_by_id',
            ('id_member_set-0-last_visit', '2016-11-23 14:47:33'),
            ('id_member_set-0-note', 'Veteran of Russian badminton'),
            'input_as_select_click', ('id_member_set-0-plays_0',),
            'input_as_select_click', ('id_member_set-0-role_1',),
            'by_id', ('id_member_set-0-is_endorsed',),
            'click',
        )


class UpdateSportClub(AutomationCommands):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.club_id = kwargs.pop('club_id')
        self. update_view = {'viewname': 'club_update', 'kwargs': {'club_id': self.club_id}}

    def open_update_form(self):
        return (
            'click_anchor_by_view', self.update_view,
            'form_by_view', self.update_view,
        )

    def test_formset_removal(self):
        return (
            'relative_form_button_click', ('Add "Sport club equipment"',),
            'by_id', ('id_equipment_set-1-DELETE',),
            'click',
            'to_top_bootstrap_dialog',
            'dialog_button_click', ('Yes',),
            'form_by_view', self.update_view,
        )

    def add_equipment_bubblelat(self):
        AddSportClubInventory
    add_equipment_bubblelat = (
        'relative_form_button_click', ('Add "Sport club equipment"',),
        'fk_widget_add_and_select', (
            'id_equipment_set-1-manufacturer',
            (
                'keys_by_id', ('id_company_name', 'Bubblelat'),
            ),
            (
                'grid_find_data_column', ('Company name', 'Bubblelat'),
            )
        ),
        'keys_by_id', ('id_equipment_set-1-inventory_name', 'Bubble Pro 2010'),
        'input_as_select_click', ('id_equipment_set-1-category_1',),
    )

    add_member_john_smith = (
        'relative_form_button_click', ('Add "Sport club member"',),
        'fk_widget_add_and_select', (
            'id_member_set-1-profile',
            (
                'keys_by_id',
                ('id_first_name', 'John',),
                ('id_last_name', 'Smith',),
                ('id_birth_date', '1973-05-19',),
            ),
            (
                'grid_find_data_column', ('First name', 'John'),
            )
        ),
        'keys_by_id',
        ('id_member_set-1-last_visit', '2016-11-27 19:27:41'),
        ('id_member_set-1-note', 'Entrepreneur and master of squash'),
        'input_as_select_click', ('id_member_set-1-plays_3',),
        'input_as_select_click', ('id_member_set-1-role_0',),
    )

    @classmethod
    def get_commands(cls):
        commands = (
            cls.open_update_form() +
            cls.test_formset_removal() +
            cls.add_equipment_bubblelat +
            cls.add_member_john_smith +
            ('click_submit_by_view', cls.update_view,)
        )
        return commands


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
        yield from AddSportClub().set_context({
            'club': {
                'title': 'Yaroslavl Bears',
                'foundation_date': '1971-08-29',
            },
        }).club_base_info()
        yield from AddSportClubInventory(formset_idx=0).set_context({
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
        yield from AddSportClubMembers(
            formset_idx=0
        ).add_member()
        yield ('click_submit_by_view', ('club_create',))

    def details_sport_club(self):
        yield (
            'button_click', ('Read',),
            'dialog_button_click', ('OK',),
        )
