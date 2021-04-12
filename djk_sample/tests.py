from django_jinja_knockout.testing import AutomationCommands, DjkSeleniumCommands, DjkTestCase

from club_app.tests import ClubAppCommands
from event_app.tests import EventAppCommands

for command in DjkSeleniumCommands.yield_command_names():
    globals()[command] = command


class DjkSampleCommands(AutomationCommands):

    def __init__(self, *args, **kwargs):
        self.testcase = kwargs.pop('testcase')
        super().__init__(*args, **kwargs)

    def register_new_user(self):
        yield (
            click_anchor_by_view, {'viewname': 'account_signup'},
            keys_by_id,
            ('id_username', self._.username),
            ('id_password1', self._.password),
            ('id_password2', self._.password),
            click_submit_by_view, ('account_signup',),
            has_messages_success,
            dump_data, ('new_user_registered',)
        )

    def logout_user(self):
        yield (
            click_anchor_by_view, {'viewname': 'account_logout'},
            click_submit_by_view, ('account_logout',),
            has_messages_success,
        )

    def login_user(self):
        yield (
            click_anchor_by_view, {'viewname': 'account_login'},
            keys_by_id,
            ('id_login', self._.username),
            ('id_password', self._.password),
            click_submit_by_view, ('account_login',),
            has_messages_success,
        )

    def user_preferences(self):
        yield (
            component_by_classpath, ('EditForm',),
            click,
            to_top_bootstrap_dialog,
            keys_by_id,
            ('id_first_name', 'Dmitriy'),
            ('id_last_name', 'Sintsov'),
            ('id_email', 'questpc256@gmail.com'),
            dialog_footer_button_click, ('Save',),
            wait_until_dialog_closes,
            to_top_bootstrap_dialog,
            dialog_footer_button_click, ('OK',),
            wait_until_dialog_closes,
        )

    def test_all(self):
        yield (
            maximize_window,
            relative_url, ('/',),
            click_anchor_by_view, {'viewname': 'renderer_test'},
        )
        if not self.testcase.has_fixture('new_user_registered'):
            yield from self.register_new_user()
            yield from self.logout_user()
        yield from self.login_user()
        yield from self.user_preferences()

        if not self.testcase.has_fixture('sport_club_updated'):
            yield from ClubAppCommands().yield_class_commands(
                'empty_club_list',
                'add_sport_club',
                'details_sport_club',
                'update_sport_club',
            )
            yield from EventAppCommands().yield_class_commands(
                'event_list_navigate',
                'event_list_preview_member',
            )
            yield from ClubAppCommands().yield_class_commands(
                'browse_preloaded_dtl_grid',
            )
        if not self.testcase.has_fixture('grid_interaction_club_actions_done'):
            yield from EventAppCommands().yield_class_commands(
                'grid_interaction_club_actions',
            )
        if not self.testcase.has_fixture('grid_interaction_club_equipment_done'):
            yield from ClubAppCommands().yield_class_commands(
                'browse_grid_with_raw_query',
                'grid_interaction_club_equipment',
            )
        if not self.testcase.has_fixture('grid_custom_actions_done'):
            yield from ClubAppCommands().yield_class_commands(
                'grid_custom_layout',
                'grid_custom_actions',
                'to_club_member_grid_page',
                # Check manual component invocation. Issued twice to check component re-instantiation.
                'manual_component_invocation',
                'manual_component_invocation',
            )


class DjkSampleTestCase(DjkTestCase):

    fixtures = []
    # fixtures = ['0000_new_user_registered.json']
    # fixtures = ['0001_sport_club_updated.json']
    # fixtures = ['0002_grid_interaction_club_actions_done.json']
    # fixtures = ['0003_grid_interaction_club_equipment_done.json']
    # fixtures = ['0004_grid_custom_actions_done.json']

    fixtures_order = [
        'new_user_registered',
        'sport_club_updated',
        'grid_interaction_club_actions_done',
        'grid_interaction_club_equipment_done',
        'grid_custom_actions_done',
    ]

    def test_all(self):
        DjkSeleniumCommands(
            testcase=self,
        ).exec_class(
            DjkSampleCommands(testcase=self).set_parameters({
                'username': 'testuser',
                'password': 'djk12345',
            }),
            'test_all'
        )._default_wait()
