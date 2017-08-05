from django_jinja_knockout.context_processors import TemplateContextProcessor as BaseContextProcessor


class TemplateContextProcessor(BaseContextProcessor):

    CLIENT_ROUTES = (
        # This route is injected into every page globally (not per view).
        # This is a good idea if some client-side route is frequently used.
        # Alternatively one can specify client route url names per view.
        # Second element of each tuple defines whether client-side route should be available to anonymous users.
        ('user_change', True),
        ('equipment_grid', True),
    )


def template_context_processor(HttpRequest=None):
    return TemplateContextProcessor(HttpRequest).get_context_data()
