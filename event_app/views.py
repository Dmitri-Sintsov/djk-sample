from django.conf import settings

from django_jinja_knockout.views import ListSortingView, ContextDataMixin

from .models import Action


class ActionList(ContextDataMixin, ListSortingView):

    model = Action
    template_name = 'action_list.htm'
    context_object_name = 'actions'
    paginate_by = settings.OBJECTS_PER_PAGE
    allowed_sort_orders = '__all__'

    def get_allowed_filter_fields(self):
        allowed_filter_fields = {
            'type': None,
            'content_type_id': self.get_contenttype_filter(
                ('club_app', 'equipment'),
                ('club_app', 'member'),
            )
        }
        return allowed_filter_fields
