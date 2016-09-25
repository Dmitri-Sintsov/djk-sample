from selenium.webdriver.firefox.webdriver import WebDriver

from django.utils.html import format_html

from django_jinja_knockout.tpl import reverseq
from django_jinja_knockout.testing import SeleniumCommands


class ClubAppTests(SeleniumCommands):
    # fixtures = ['user-data.json']

    @classmethod
    def selenium_factory(cls):
        return WebDriver()

    def do_has_messages_success(self):
        return self.do_by_xpath('//div[@class="messages"]/div[@class="alert alert-danger success"]')

    def register_new_user(self):
        self.exec(
            'reverse_url', {'viewname': 'account_signup'},
            'keys_by_id', ('id_username', 'testuser'),
                ('id_password1', 'test123'),
                ('id_password2', 'test123'),
            'find_submit_by_viewname', ('account_signup',),
            'click',
            'has_messages_success',
        )

    def logout_user(self):
        self.exec(
            'reverse_url', {'viewname': 'account_logout'},
            'find_submit_by_viewname', ('account_logout',),
            'click',
            'has_messages_success',
        )

    def login_user(self):
        self.exec(
            'reverse_url', {'viewname': 'account_login'},
            'keys_by_id', ('id_login', 'testuser'),
            ('id_password', 'test123'),
            'find_submit_by_viewname', ('account_login',),
            'click',
            'has_messages_success',
        )

    def add_sport_club(self):
        self.exec(
            'reverse_url', {'viewname': 'club_create'}
        )

    def test_signup(self):
        from selenium.webdriver.support.wait import WebDriverWait
        timeout = self.__class__.WAIT_SECONDS
        self.register_new_user()
        self.logout_user()
        self.login_user()
        # self.add_sport_club()
