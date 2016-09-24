from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver

from django_jinja_knockout.tpl import reverseq


class SeleniumMixin:
    pass


class ClubAppTests(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(20)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def get_reverse_url(self, viewname, kwargs=None, query=None):
        url = '{}{}'.format(
            self.live_server_url, reverseq(viewname=viewname, kwargs=kwargs, query=query)
        )
        print('get_reverse_url: {}'.format(url))
        return self.selenium.get(url)

    def test_signup(self):
        from selenium.webdriver.support.wait import WebDriverWait
        timeout = 20
        self.get_reverse_url('account_signup')

        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys('testuser')
        password_input = self.selenium.find_element_by_id("id_password1")
        password_input.send_keys('test123')
        password_input = self.selenium.find_element_by_id("id_password2")
        password_input.send_keys('test123')

        self.selenium.find_element_by_xpath('//input[@value="Sign Up »"]').click()
