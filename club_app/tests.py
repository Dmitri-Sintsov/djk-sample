from selenium.webdriver.firefox.webdriver import WebDriver

from django.utils.html import format_html

from django_jinja_knockout.tpl import reverseq
from django_jinja_knockout.viewmodels import to_json
from django_jinja_knockout.testing import SeleniumCommands


class ClubAppTests(SeleniumCommands):
    # fixtures = ['user-data.json']

    @classmethod
    def selenium_factory(cls):
        return WebDriver()

    def do_has_messages_success(self):
        return self.do_by_xpath('//div[@class="messages"]/div[@class="alert alert-danger success"]')

    def do_jumbotron_text(self, text):
        return self.do_by_xpath(
            '//div[@class="jumbotron"]/div[@class="default-padding" and contains(text(), "{}")]'.format(text),
        )

    def do_input_as_select_click(self, id):
        self.exec(
            'by_id', (id,),
            'element_by_xpath', ('parent::label',),
            'click',
        )
        return self.last_result

    def do_fk_widget_click(self, id):
        self.exec(
            'by_id', (id,),
            'element_by_xpath', ('following-sibling::button',),
            'click',
            'to_active_element',
        )
        return self.last_result

    def do_grid_dialog_button_action_click(self, action_name):
        self.exec(
            'by_classname', ('bootstrap-dialog-message',),
            'element_by_xpath', ('//span[text()="{}"]/parent::button'.format(action_name),),
            'click',
        )
        return self.last_result

    def do_dialog_button_click(self, button_title):
        self.exec(
            'to_active_element',
            'element_by_xpath',
                ('//div[@class="bootstrap-dialog-footer"]//button[contains(., "{}")]'.format(button_title),),
            'click'
        )
        return self.last_result

    def register_new_user(self):
        self.exec(
            'reverse_url', {'viewname': 'account_signup'},
            'keys_by_id',
                ('id_username', 'testuser'),
                ('id_password1', 'test123'),
                ('id_password2', 'test123'),
            'find_submit_by_view', ('account_signup',),
            'click',
            'has_messages_success',
        )

    def logout_user(self):
        self.exec(
            'reverse_url', {'viewname': 'account_logout'},
            'find_submit_by_view', ('account_logout',),
            'click',
            'has_messages_success',
        )

    def login_user(self):
        self.exec(
            'reverse_url', {'viewname': 'account_login'},
            'keys_by_id',
                ('id_login', 'testuser'),
                ('id_password', 'test123'),
            'find_submit_by_view', ('account_login',),
            'click',
            'has_messages_success',
        )

    def empty_club_list(self):
        self.exec(
            'reverse_url', {'viewname': 'club_list'},
            'jumbotron_text', ('There is no',),
            'find_anchor_by_view', (
                'club_list',
                {},
                {
                    'list_filter': to_json({
                        'category': 1
                    })
                }
            ),
            'click',
            'jumbotron_text', ('There is no',),
            'reverse_url', (
                'club_list',
                {},
                {
                    'list_filter': to_json({
                        'category1': 1
                    })
                }
            ),
            'jumbotron_text', ('Not allowed filter field',),
        )

    def add_sport_club(self):
        self.exec(
            'reverse_url', {'viewname': 'club_create'},
            'keys_by_id',
                ('id_title', 'Yaroslavl Bears'),
                ('id_foundation_date', '1971-08-29'),
            'input_as_select_click', ('id_category_1',),
            'fk_widget_click', ('id_equipment_set-0-manufacturer',),
            'grid_dialog_button_action_click', ('Add',),
            'dialog_button_click', ('Save',),
        )

    def test_signup(self):
        from selenium.webdriver.support.wait import WebDriverWait
        timeout = self.__class__.WAIT_SECONDS
        self.register_new_user()
        self.logout_user()
        self.login_user()
        self.empty_club_list()
        self.add_sport_club()
