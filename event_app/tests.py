from django_jinja_knockout.viewmodels import to_json
from django_jinja_knockout.automation import AutomationCommands
from django_jinja_knockout.testing import DjkSeleniumCommands
from club_app.testing import SportClub, SportClubInventory, SportClubMembers

for command in DjkSeleniumCommands.yield_command_names():
    globals()[command] = command


class EventAppCommands(AutomationCommands):

    event_list_navigate = (
        click_anchor_by_view, {'viewname': 'action_list'},
        click_anchor_by_view, (
            'action_list',
            {},
            {
                'page': 2,
            }
        ),
        click_anchor_by_view, (
            'action_list',
            {},
            {
                'list_filter': to_json({
                    'action_type': 0,
                })
            }
        ),
        click_anchor_by_view, (
            'action_list',
            {},
            {
                'list_filter': to_json({
                    'action_type': 0,
                }),
                'page': 3,
            }
        ),
        # Check the selection of one filter multiple choices in ListSortingView:
        click_by_link_text, ('Sport club equipment',),
        click_by_link_text, ('Sport club member',),
    )

    event_list_preview_member = (
        click_anchor_by_view, (
            'member_detail',
            {
                'member_id': 2,
            },
        ),
        button_click, ('Read',),
        dialog_footer_button_click, ('OK',),
        wait_until_dialog_closes,
    )

    # Check multiple grids interaction for updating ActionGrid via result of ClubGrid action,
    # used as interactive event logging in this test case.
    # Check ActionGrid row removal.
    def grid_interaction_club_actions(self):
        yield [
            click_anchor_by_view, ('club_grid_with_action_logging', {'action': ''}),
            component_by_classpath, ('App.ko.ClubGrid',),
            grid_search_substring, ('Yaro',),
            component_by_classpath, ('App.ko.ClubGrid',),
            relative_button_click, ('Add',),
        ]
        yield from SportClub().set_parameters({
            'club': {
                'title': 'Broadway Singers',
                'category_id': 0,
                'foundation_date': '1983-11-21',
            },
        }).yield_class_commands(
            'club_base_info'
        )
        yield from SportClubInventory(formset_idx=0).set_parameters({
            'manufacturers': [
                {
                    '_create_': False,
                    'company_name': 'Yanix',
                    # 'direct_shipping': True,
                    'inventories': [
                        {
                            'name': 'FeatherSky 2021',
                            'category_id': 2,
                        },
                    ]
                },
            ]
        }).add_manufacturers()
        yield from SportClubMembers(
            formset_idx=0
        ).set_parameters({
            'members': [
                {
                    '_create_profile_': False,
                    'first_name': 'John',
                    'last_name': 'Smith',
                    # 'birth_date': '1973-05-19',
                    'last_visit': '2011-10-21 08:59:59',
                    'note': 'Founder of the most prominent NY badminton club.',
                    'plays': 0,
                    'role': 0,
                    'is_endorsed': True,
                },
            ]
        }).yield_class_commands(
            # 'new_formset_form',
            'add_members'
        )
        yield (
            dialog_footer_button_click, ('Save',),
            wait_until_dialog_closes,
            click_anchor_by_view, ('club_detail', {'club_id': 2}),
            switch_to_last_window,
            button_click, ('Read',),
            dialog_footer_button_click, ('OK',),
            wait_until_dialog_closes,
            close_current_window,
            component_by_classpath, ('App.ko.Grid',),
            # Commented out, because xpath cannot match outerHTML.
            # grid_find_data_row, ({'Related object': '<a href="/equipment-detail-5/" target="_blank">Sport club equipment</a>'},),
            component_relative_by_xpath, (
                ".//tr [ .//td[@data-caption={}]/a[@href={}] ]",
                'Related object', '/equipment-detail-5/',
            ),
            element_is_grid_row,
            # grid_select_current_row,
            grid_row_glyphicon_action, ('Remove',),
            dialog_footer_button_click, ('Yes',),
            dump_data, ('grid_interaction_club_actions_done',),
        )
