from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from django_jinja_knockout.testing import DjkSeleniumCommands

from club_app.tests import ClubAppCommands


class DjkSampleCommands(DjkSeleniumCommands):

    def register_new_user(self):
        self.exec(
            'relative_url', ('/',),
            'click_anchor_by_view', {'viewname': 'account_signup'},
            'keys_by_id',
            ('id_username', self._.username),
            ('id_password1', self._.password),
            ('id_password2', self._.password),
            'click_submit_by_view', ('account_signup',),
            'has_messages_success',
        )

    def logout_user(self):
        self.exec(
            'click_anchor_by_view', {'viewname': 'account_logout'},
            'click_submit_by_view', ('account_logout',),
            'has_messages_success',
        )

    def login_user(self):
        self.exec(
            'click_anchor_by_view', {'viewname': 'account_login'},
            'keys_by_id',
            ('id_login', self._.username),
            ('id_password', self._.password),
            'click_submit_by_view', ('account_login',),
            'has_messages_success',
        )

    def test_all(self):
        self._maximize_window()
        self.register_new_user()
        # self.logout_user()
        # self.login_user()
        self.exec_class(
            ClubAppCommands(),
            'empty_club_list',
            'add_sport_club',
            'details_sport_club',
            # 'update_sport_club',
        )
        self._default_sleep()


class DjkSampleTestCase(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    WAIT_SECONDS = 5

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
        DjkSampleCommands(testcase=self).set_context({
            'username': 'testuser',
            'password': 'test123',
        }).test_all()
