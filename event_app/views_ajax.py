from collections import OrderedDict

from django.utils.html import format_html

from django_jinja_knockout.views import KoGridView

from .models import Action


class ActionGrid(KoGridView):

    model = Action
    grid_fields = [
        'performer',
        'date',
        'action_type',
        'content_object'
    ]
    allowed_sort_orders = [
        'performer',
        'date',
        'action_type',
    ]
    mark_safe_fields = [
        'content_object'
    ]

    def get_allowed_filter_fields(self):
        allowed_filter_fields = OrderedDict([
            ('action_type', None),
            ('content_type', self.get_contenttype_filter(
                ('club_app', 'club'),
                ('club_app', 'equipment'),
                ('club_app', 'member'),
            ))
        ])
        return allowed_filter_fields

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
    def get_row_str_fields(self, obj, row):
        str_fields = super().get_row_str_fields(obj, row)
        if str_fields is None:
            str_fields = {}
        # Add formatted display of virtual field.
        if hasattr(obj.content_object, 'get_canonical_link'):
            str_fields['content_object'] = format_html(
                '<a href="{1}">{0}</a>',
                *obj.content_object.get_canonical_link()
            )
        return str_fields
