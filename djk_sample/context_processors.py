from django_jinja_knockout.context_processors import TemplateContextProcessor as BaseContextProcessor


def template_context_processor(HttpRequest=None):
    return BaseContextProcessor(HttpRequest).get_context_data()
