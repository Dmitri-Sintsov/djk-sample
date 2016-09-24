from selenium.webdriver.firefox.webdriver import WebDriver

from django_jinja_knockout.testing import SeleniumCommands


class ClubAppTests(SeleniumCommands):
    # fixtures = ['user-data.json']

    @classmethod
    def selenium_factory(cls):
        return WebDriver()

    def test_signup(self):
        from selenium.webdriver.support.wait import WebDriverWait
        timeout = self.__class__.WAIT_SECONDS

        self.exec(
            'reverse_url', {'viewname': 'account_signup'},
            'keys_by_id', ('id_username', 'testuser'),
                ('id_password1', 'test123'),
                ('id_password2', 'test123'),
            'by_xpath', ('//form[@class="signup"]//button[@type="submit"]',),
            'click'
        )
