from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver

from django_jinja_knockout.tpl import reverseq


"""
Selenium tests may require Firefox ESR because Ubuntu sometimes updates Firefox to newer version
than currently installed Selenium supports.

Here is the example of installing Firefox ESR in Ubuntu 14.04:

apt-get remove firefox
wget http://ftp.mozilla.org/pub/firefox/releases/45.4.0esr/linux-x86_64/en-US/firefox-45.4.0esr.tar.bz2
tar -xvjf firefox-45.4.0esr.tar.bz2 -C /opt
ln -s /opt/firefox/firefox /usr/bin/firefox

Do not forget to update to latest ESR when running the tests.
"""


class SeleniumMixin:

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

    def keys_by_id(self, id, keys, *args):
        input = self.selenium.find_element_by_id(id)
        input.send_keys(keys)
        if len(args) > 0:
            for _id, _keys in zip(args[::2], args[1::2]):
                yield self.keys_by_id(_id, _keys)
            yield input
        else:
            return input


class ClubAppTests(SeleniumMixin, StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    def test_signup(self):
        from selenium.webdriver.support.wait import WebDriverWait
        timeout = 20
        self.get_reverse_url('account_signup')

        self.keys_by_id(
            'id_username', 'testuser',
            'id_password1', 'test123',
            'id_password2', 'test123'
        )

        self.selenium.find_element_by_xpath('//form[@class="signup"]//button[@type="submit"]').click()
