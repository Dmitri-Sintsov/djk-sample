import re
from django_jinja_knockout.middleware import ContextMiddleware as BaseContextMiddleware


class ContextMiddleware(BaseContextMiddleware):

    def is_our_module(self, module):
        return super().is_our_module(module) or re.match(r'^club_', module)
