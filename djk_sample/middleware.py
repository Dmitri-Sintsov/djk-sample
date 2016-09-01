from django_jinja_knockout.middleware import ContextMiddleware as BaseContextMiddleware


class ContextMiddleware(BaseContextMiddleware):

    def add_action(self, obj, action_type):
        request = self.get_request()
        if not hasattr(request, 'actions'):
            request.actions = []
        request.actions.append((obj, action_type))

    def save_actions(self):
        request = self.get_request()
        if hasattr(request, 'actions'):
            from event_app.models import Action
            for args in request.actions:
                Action.do(*args)
