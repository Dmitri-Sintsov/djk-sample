from django_jinja_knockout.viewmodels import to_json
from django_jinja_knockout.automation import AutomationCommands
from django_jinja_knockout.testing import DjkSeleniumCommands
from .testing import SportClub, SportClubInventory, SportClubMembers

for command in DjkSeleniumCommands.yield_command_names():
    globals()[command] = command


class ClubAppCommands(AutomationCommands):

    empty_club_list = (
        click_anchor_by_view, {'viewname': 'club_list'},
        jumbotron_text, ('There is no',),
        click_anchor_by_view, (
            'club_list',
            {},
            {
                'list_filter': to_json({
                    'category': 1
                })
            }
        ),
        jumbotron_text, ('There is no',),
        reverse_url, (
            'club_list',
            {},
            {
                'list_filter': to_json({
                    'category1': 1
                })
            }
        ),
        jumbotron_text, ('Not allowed filter field',),
    )

    def add_sport_club(self):
        form_view = ('club_create',)
        yield from SportClub().set_parameters({
            'form_view': form_view,
            'club': {
                'title': 'Yaroslavl Bears',
                'category_id': 1,
                'foundation_date': '1971-08-29',
            },
        }).yield_class_commands(
            'club_form_view',
            'club_base_info'
        )
        yield from SportClubInventory(formset_idx=0).set_parameters({
            'manufacturers': [
                {
                    '_create_': True,
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
                    '_create_': True,
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
        ).set_parameters({
            'members': [
                {
                    '_create_profile_': True,
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
                    '_create_profile_': True,
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
        yield (click_submit_by_view, form_view)

    def details_sport_club(self):
        yield (
            button_click, ('Read',),
            dialog_button_click, ('OK',),
            wait_until_dialog_closes,
        )

    def update_sport_club(self):
        form_view = {'viewname': 'club_update', 'kwargs': {'club_id': 1}}
        yield from SportClub().set_parameters({
            'form_view': form_view,
        }).yield_class_commands(
            'club_form_view',
            'club_base_info'
        )
        yield from SportClubInventory(formset_idx=3).set_parameters({
            'form_view': form_view,
            'manufacturers': [
                {
                    '_create_': True,
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
        ).set_parameters({
            'members': [
                {
                    '_create_profile_': True,
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
        yield (
            click_submit_by_view, (form_view),
            dump_data, ('sport_club_updated',)
        )

    browse_grid_with_raw_query = (
        click_anchor_by_view, ('club_grid_raw_query', {'action': ''}),
        component_by_classpath, ('App.ko.Grid',),
        # Test JOINed field queries.
        grid_order_by, ('First name',),
        grid_goto_page, ('2',),
        grid_find_data_row, ({'First name': 'Liu', 'Title': 'Yaroslavl Bears'},),
        grid_breadcrumb_filter_choices, ('Category', ['Recreational']),
        grid_breadcrumb_filter_choices, ('Role', ['Owner', 'Member']),
        grid_find_data_row, ({'First name': 'Ivan', 'Title': 'Broadway Singers'},),
    )

    def grid_interaction_club_equipment(self):
        yield (
            click_anchor_by_view, ('club_equipment_grid', {'action': ''}),
            component_by_classpath, ('App.ko.ClubGrid',),
            grid_find_data_row, ({'Title': 'Broadway Singers'},),
            grid_row_glyphicon_action, ('Add club equipment',),
        )
        yield from SportClubInventory(formset_idx=None).set_parameters({
            'manufacturers': [
                {
                    '_create_': True,
                    'company_name': 'Vector',
                    'direct_shipping': False,
                    'inventories': [
                        {
                            'name': 'CourageousWave 100',
                            'category_id': 3,
                        },
                    ]
                },
            ]
        }).add_manufacturers()
        yield (
            dialog_button_click, ('Save',),
            wait_until_dialog_closes,
            click_by_link_text, ('Sport club equipments',),
            component_by_id, ('equipment_grid',),
            grid_find_data_row, ({'Company name': 'Vector', 'Inventory name': 'CourageousWave 100'},),
            dump_data, ('grid_interaction_club_equipment_done',),
        )

    def grid_custom_layout_and_custom_actions(self):
        yield (
            click_anchor_by_view, ('member_grid_custom_actions', {'action': ''}),
        )
