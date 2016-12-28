from django_jinja_knockout.middleware import ContextMiddleware as BaseContextMiddleware


class ContextMiddleware(BaseContextMiddleware):

    def add_action(self, obj, action_type):
        self.__class__.add_instance('actions', (obj, action_type))

    def save_actions(self, request):
        from event_app.models import Action
        for args in self.__class__.yield_out_instances('actions'):
            Action.do(*args)

    def process_view(self, request, view_func, view_args, view_kwargs):
        result = super().process_view(request, view_func, view_args, view_kwargs)
        self.save_actions(request)
        return result
