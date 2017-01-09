import os
from selenium.webdriver.firefox.webdriver import WebDriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.utils import override_settings
from django.conf import settings

from django_jinja_knockout.testing import AutomationCommands, DjkSeleniumCommands

from club_app.tests import ClubAppCommands
from event_app.tests import EventAppCommands


class DjkSampleCommands(AutomationCommands):

    def __init__(self, *args, **kwargs):
        self.testcase = kwargs.pop('testcase')
        super().__init__(*args, **kwargs)

    def register_new_user(self):
        yield (
            'click_anchor_by_view', {'viewname': 'account_signup'},
            'keys_by_id',
            ('id_username', self._.username),
            ('id_password1', self._.password),
            ('id_password2', self._.password),
            'click_submit_by_view', ('account_signup',),
            'has_messages_success',
            'dump_data', ('new_user_registered',)
        )

    def logout_user(self):
        yield (
            'click_anchor_by_view', {'viewname': 'account_logout'},
            'click_submit_by_view', ('account_logout',),
            'has_messages_success',
        )

    def login_user(self):
        yield (
            'click_anchor_by_view', {'viewname': 'account_login'},
            'keys_by_id',
            ('id_login', self._.username),
            ('id_password', self._.password),
            'click_submit_by_view', ('account_login',),
            'has_messages_success',
        )

    def test_all(self):
        yield (
            'maximize_window',
            'relative_url', ('/',),
        )
        if not self.testcase.has_fixture_prefix('sport_club_updated'):
            yield from self.register_new_user()
            yield from self.logout_user()
        yield from self.login_user()

        if not self.testcase.has_fixture_prefix('sport_club_updated'):
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


@override_settings(DEBUG=True)
class DjkSampleTestCase(StaticLiveServerTestCase):
    fixtures = []
    # fixtures = ['sport_club_updated_2017-01-09_16-03-42-236662.json']

    reset_sequences = True

    WAIT_SECONDS = 5

    def has_fixture_prefix(self, prefix):
        for fixture in self.fixtures:
            if fixture.startswith(prefix):
                return True
        return False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = cls.selenium_factory()
        cls.selenium.implicitly_wait(cls.WAIT_SECONDS)

    @classmethod
    def tearDownClass(cls):
        # cls.selenium.quit()
        super().tearDownClass()

    @classmethod
    def selenium_factory(cls):
        return WebDriver()

    def test_all(self):
        DjkSeleniumCommands(testcase=self).exec_class(
            DjkSampleCommands(testcase=self).set_context({
                'username': 'testuser',
                'password': 'test123',
            }),
            'test_all'
        )._default_sleep()
