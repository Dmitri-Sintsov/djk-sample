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
            'relative_url', ('/',),
            'click_anchor_by_view', {'viewname': 'account_signup'},
            'keys_by_id',
                ('id_username', 'testuser'),
                ('id_password1', 'test123'),
                ('id_password2', 'test123'),
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
                ('id_login', 'testuser'),
                ('id_password', 'test123'),
            'click_submit_by_view', ('account_login',),
            'has_messages_success',
        )

    def empty_club_list(self):
        self.exec(
            'click_anchor_by_view', {'viewname': 'club_list'},
            'jumbotron_text', ('There is no',),
            'click_anchor_by_view', (
                'club_list',
                {},
                {
                    'list_filter': to_json({
                        'category': 1
                    })
                }
            ),
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

    class AddSportClub:

        club_yaroslavl_bears_base_info = (
            'click_anchor_by_view', {'viewname': 'club_create'},
            # Next one step is optional:
            'form_by_view', ('club_create',),
            'keys_by_id',
            ('id_title', 'Yaroslavl Bears'),
            ('id_foundation_date', '1971-08-29'),
            'input_as_select_click', ('id_category_1',),
        )

        add_manufacturer_yanex = (
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
        )

        add_member_ivan_petrov = (
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
        )

        @classmethod
        def get_commands(cls):
            commands = (
                cls.club_yaroslavl_bears_base_info +
                cls.add_manufacturer_yanex +
                cls.add_member_ivan_petrov +
                ('click_submit_by_view', ('club_create',),)
            )
            return commands

    def details_sport_club(self):
        self.exec(
            'button_click', ('Read',),
            'dialog_button_click', ('OK',),
        )

    class UpdateSportClub:

        update_view = {'viewname': 'club_update', 'kwargs': {'club_id': 1}}

        @classmethod
        def open_update_form(cls):
            return (
                'click_anchor_by_view', cls.update_view,
                'form_by_view', cls.update_view,
            )

        @classmethod
        def test_formset_removal(cls):
            return (
                'relative_form_button_click', ('Add "Sport club equipment"',),
                'by_id', ('id_equipment_set-1-DELETE',),
                'click',
                'to_top_bootstrap_dialog',
                'dialog_button_click', ('Yes',),
                'form_by_view', cls.update_view,
            )

        add_equipment_bubblelat = (
            'relative_form_button_click', ('Add "Sport club equipment"',),
            'fk_widget_add_and_select', (
                'id_equipment_set-1-manufacturer',
                (
                    'keys_by_id', ('id_company_name', 'Bubblelat'),
                ),
                (
                    'grid_find_data_column', ('Company name', 'Bubblelat'),
                )
            ),
            'keys_by_id', ('id_equipment_set-1-inventory_name', 'Bubble Pro 2010'),
            'input_as_select_click', ('id_equipment_set-1-category_1',),
        )

        add_member_john_smith = (
            'relative_form_button_click', ('Add "Sport club member"',),
            'fk_widget_add_and_select', (
                'id_member_set-1-profile',
                (
                    'keys_by_id',
                    ('id_first_name', 'John',),
                    ('id_last_name', 'Smith',),
                    ('id_birth_date', '1973-05-19',),
                ),
                (
                    'grid_find_data_column', ('First name', 'John'),
                )
            ),
            'keys_by_id',
            ('id_member_set-1-last_visit', '2016-11-27 19:27:41'),
            ('id_member_set-1-note', 'Entrepreneur and master of squash'),
            'input_as_select_click', ('id_member_set-1-plays_3',),
            'input_as_select_click', ('id_member_set-1-role_0',),
        )

        @classmethod
        def get_commands(cls):
            commands = (
                cls.open_update_form() +
                cls.test_formset_removal() +
                cls.add_equipment_bubblelat +
                cls.add_member_john_smith +
                ('click_submit_by_view', cls.update_view,)
            )
            return commands

    def test_all(self):
        self._maximize_window()
        self.register_new_user()
        self.logout_user()
        self.login_user()
        self.empty_club_list()
        self.exec_class(self.__class__.AddSportClub)
        self.details_sport_club()
        self.exec_class(self.__class__.UpdateSportClub)
        self._default_sleep()
