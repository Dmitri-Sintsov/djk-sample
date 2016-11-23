from selenium.webdriver.firefox.webdriver import WebDriver

from django.utils.html import format_html

from django_jinja_knockout.tpl import reverseq
from django_jinja_knockout.viewmodels import to_json
from django_jinja_knockout.testing import DjkSeleniumCommands


class ClubAppTests(DjkSeleniumCommands):
    # fixtures = ['user-data.json']

    @classmethod
    def selenium_factory(cls):
        return WebDriver()

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
            'fk_widget_add_and_select', (
                'id_equipment_set-0-manufacturer',
                (
                    'dialog_button_click', ('Save',),
                    'assert_field_error', ('id_company_name', 'This field is required.'),
                    'keys_by_id', ('id_company_name', 'Yanex'),
                    'by_id', ('id_direct_shipping',),
                    'click',
                ),
                (
                    'grid_find_data_column', ('Company name', 'Yanex'),
                )
            ),
            'keys_by_id', ('id_equipment_set-0-inventory_name', 'Silent Air 2020'),
            'input_as_select_click', ('id_equipment_set-0-category_2',),
            'relative_form_button_click', ('Add "Sport club member"',),
            'fk_widget_add_and_select', (
                'id_member_set-0-profile',
                (
                    'keys_by_id',
                        ('id_first_name', 'Ivan',),
                        ('id_last_name', 'Petrov',),
                        ('id_birth_date', '1971-07-29',),
                ),
                (
                    'grid_find_data_column', ('First name', 'Ivan'),
                )
            ),
            'keys_by_id',
                ('id_member_set-0-last_visit', '2016-11-23 14:47:33'),
                ('id_member_set-0-note', 'Veteran of Russian badminton'),
            'input_as_select_click', ('id_member_set-0-plays_0',),
            'input_as_select_click', ('id_member_set-0-role_1',),
            'by_id', ('id_member_set-0-is_endorsed',),
            'click',
            'find_submit_by_view', ('club_create',),
            'click',
        )

    def test_all(self):
        self.register_new_user()
        self.logout_user()
        self.login_user()
        self.empty_club_list()
        self.add_sport_club()
