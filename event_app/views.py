from django_jinja_knockout.views import ListSortingView

from .models import Action


class ActionList(ListSortingView):
    # Enabled always visible paginator links because there could be many pages of actions, potentially.
    always_visible_links = True
    model = Action
    grid_fields = [
        [
            'performer',
            'performer__is_superuser',
            'date',
        ],
        'action_type',
        'content_object'
    ]
    allowed_sort_orders = [
        'performer',
        'date',
        'action_type',
    ]

    def get_allowed_filter_fields(self):
        allowed_filter_fields = {
            # Override default templates for filter fields:
            'action_type': {'template': 'bs_navs.htm'},
            # Specify custom client-side Javascript component class to extend it's functionality:
            'id': {
                'component_class': 'ListRangeFilter',
            },
            'date': {},
            # Generate widget choices for contenttypes framework:
            'content_type': self.get_contenttype_filter(
                ('club_app', 'club'),
                ('club_app', 'equipment'),
                ('club_app', 'member'),
            ),
        }
        return allowed_filter_fields
