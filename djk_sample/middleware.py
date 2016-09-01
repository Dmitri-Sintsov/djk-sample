from django_jinja_knockout.middleware import ContextMiddleware as BaseContextMiddleware


class ContextMiddleware(BaseContextMiddleware):

    def add_action(self, obj, action_type):
        request = self.get_request()
        if not hasattr(request, 'actions'):
            request.actions = []
        request.actions.append((obj, action_type))

    def save_actions(self, request):
        if hasattr(request, 'actions'):
            from event_app.models import Action
            for args in request.actions:
                Action.do(*args)

    def process_view(self, request, view_func, view_args, view_kwargs):
        result = super().process_view(request, view_func, view_args, view_kwargs)
        self.save_actions(request)
        return result
