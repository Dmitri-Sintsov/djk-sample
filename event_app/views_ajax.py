from collections import OrderedDict

from django.utils.html import format_html
from django.contrib.auth.models import User

from django_jinja_knockout.tpl import format_local_date
from django_jinja_knockout.views import KoGridView

from .models import Action


class UserFkWidgetGrid(KoGridView):

    model = User
    grid_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'is_superuser',
        'is_staff',
        'is_active',
        'last_login',
        'date_joined',
    ]
    search_fields = [
        ('username', 'contains'),
        ('first_name', 'icontains'),
        ('last_name', 'icontains'),
    ]
    allowed_sort_orders = '__all__'
    allowed_filter_fields = OrderedDict([
        ('is_superuser', None),
        ('is_staff', None),
        ('is_active', None),
        ('last_login', None),
        ('date_joined', None),
    ])

    # Optional formatting of virtual field (not required).
    def get_row_str_fields(self, obj, row=None):
        str_fields = {
            'last_login': format_local_date(obj.last_login),
            'date_joined': format_local_date(obj.date_joined),
        }
        return str_fields


class ActionGrid(KoGridView):

    client_routes = [
        'user_fk_widget_grid'
    ]
    model = Action
    grid_fields = [
        'performer',
        'date',
        'action_type',
        'content_type',
        'content_object'
    ]
    allowed_sort_orders = [
        'performer',
        'date',
        'action_type',
    ]
    mark_safe_fields = [
        'content_type'
    ]
    enable_deletion = True

    def get_allowed_filter_fields(self):
        allowed_filter_fields = OrderedDict([
            ('performer', None),
            ('date', None),
            ('action_type', None),
            ('content_type', self.get_contenttype_filter(
                ('club_app', 'club'),
                ('club_app', 'equipment'),
                ('club_app', 'member'),
            ))
        ])
        return allowed_filter_fields

    def get_field_verbose_name(self, field_name):
        if field_name == 'content_object':
            return 'Object description'
        else:
            return super().get_field_verbose_name(field_name)

    def get_related_fields(self, query_fields=None):
        query_fields = super().get_related_fields(query_fields)
        # Remove virtual field from queryset values().
        query_fields.remove('content_object')
        return query_fields

    def postprocess_row(self, row, obj):
        # Add virtual field value.
        content_object = obj.content_object
        row['content_object'] = content_object.get_str_fields() \
            if hasattr(content_object, 'get_str_fields') \
            else str(content_object)
        row = super().postprocess_row(row, obj)
        return row

    # Optional formatting of virtual field (not required).
    def get_row_str_fields(self, obj, row=None):
        if row is not None and not isinstance(row, dict):
            raise ValueError('row value should be None or dict')
        str_fields = super().get_row_str_fields(obj, row)
        if str_fields is None:
            str_fields = {}
        # Add formatted display of virtual field.
        if hasattr(obj.content_object, 'get_canonical_link'):
            desc, link = obj.content_object.get_canonical_link()
            str_fields['content_type'] = format_html(
                '<a href="{}" target="_blank">{}</a>',
                link,
                str_fields['content_type']
            )
        return str_fields

    @classmethod
    def get_default_grid_options(cls):
        return {
            'selectMultipleRows': True,
            'highlightMode': 1,
            'fkGridOptions': {
                'performer': {
                    'pageRoute': 'user_fk_widget_grid',
                    # Optional setting for BootstrapDialog:
                    'dialogOptions': {'size': 'size-wide'},
                }
            }
        }
