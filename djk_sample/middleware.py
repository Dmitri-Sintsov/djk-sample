from django_jinja_knockout.middleware import ContextMiddleware as BaseContextMiddleware


class ContextMiddleware(BaseContextMiddleware):

    def add_action(self, obj, action_type):
        self.__class__.add_instance('actions', (obj, action_type))

    def save_actions(self):
        from event_app.models import Action
        for args in self.__class__.yield_out_instances('actions'):
            Action.do(*args)

    def djk_view(self, view_func, view_args, view_kwargs):
        result = super().djk_view(view_func, view_args, view_kwargs)
        self.save_actions()
        return result
