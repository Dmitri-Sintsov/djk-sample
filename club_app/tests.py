from selenium.webdriver.firefox.webdriver import WebDriver

from django_jinja_knockout.tpl import reverseq
from django_jinja_knockout.testing import SeleniumCommands


class ClubAppTests(SeleniumCommands):
    # fixtures = ['user-data.json']

    @classmethod
    def selenium_factory(cls):
        return WebDriver()

    def register_new_user(self):
        self.exec(
            'reverse_url', {'viewname': 'account_signup'},
            'keys_by_id', ('id_username', 'testuser'),
                ('id_password1', 'test123'),
                ('id_password2', 'test123'),
            'by_xpath', ('//form[@class="signup"]//button[@type="submit"]',),
            'click',
            'by_xpath', ('//div[@class="messages"]/div[@class="alert alert-danger success"]',)
        )

    def logout_user(self):
        self.exec(
            'reverse_url', {'viewname': 'account_logout'},
            'by_xpath', (
                '//form[@action="{action}"]//button[@type="submit"]'.format(
                    action=reverseq('account_logout')
                ),
            ),
            'click',
            'by_xpath', ('//div[@class="messages"]/div[@class="alert alert-danger success"]',)
        )

    def login_user(self):
        self.exec(
            'reverse_url', {'viewname': 'account_login'},
            'keys_by_id', ('id_login', 'testuser'),
            ('id_password', 'test123'),
            'by_xpath', (
                '//form[@action="{action}"]//button[@type="submit"]'.format(
                    action=reverseq('account_login')
                ),
            ),
            'click',
            'by_xpath', ('//div[@class="messages"]/div[@class="alert alert-danger success"]',)
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
        self.add_sport_club()
