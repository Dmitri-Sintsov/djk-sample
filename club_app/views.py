from django.shortcuts import render
from django_jinja_knockout.views import InlineCreateView
from .forms import ClubFormWithInlineFormsets


def main_page(request):
    if request.method == 'GET':
        return render(request, 'main.htm')


class ClubCreate(InlineCreateView):

    template_name = 'club_create.htm'
    form_with_inline_formsets = ClubFormWithInlineFormsets
