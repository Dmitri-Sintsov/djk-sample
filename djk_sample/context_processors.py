from django_jinja_knockout.context_processors import TemplateContextProcessor as BaseContextProcessor


class TemplateContextProcessor(BaseContextProcessor):
    # An example of overriding djk context processor.
    pass


def template_context_processor(HttpRequest=None):
    return TemplateContextProcessor(HttpRequest).get_context_data()
