from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.conf import settings
from django.shortcuts import render

from django_jinja_knockout.tpl import format_local_date
from django_jinja_knockout.views import (
    FormDetailView, InlineCreateView, InlineDetailView, ListSortingView, BsTabsMixin, ContextDataMixin
)

from event_app.actions import Action

from .models import Club, Equipment, Member
from .forms import EquipmentDisplayForm, MemberDisplayForm, ClubFormWithInlineFormsets, ClubDisplayFormWithInlineFormsets


def main_page(request):
    if request.method == 'GET':
        return render(request, 'main.htm')


class ClubNavsMixin(BsTabsMixin):

    def get_main_navs(self, request, object_id=None):
        main_navs = [
            {'url': reverse('club_list'), 'text': 'List of clubs'},
            {'url': reverse('club_create'), 'text': 'Create new club'}
        ]
        if object_id is not None:
            main_navs.extend([
                {
                    'url': reverse('club_detail', kwargs={'club_id': object_id}),
                    'text': format_html('View "{}"', self.object.title)
                },
                {
                    'url': reverse('club_update', kwargs={'club_id': object_id}),
                    'text': format_html('Edit "{}"', self.object.title)
                }
            ])
        return main_navs


class ClubEditMixin(ClubNavsMixin):

    client_routes = [
        'manufacturer_fk_widget_grid',
        'profile_fk_widget_grid'
    ]
    template_name = 'club_edit.htm'
    form_with_inline_formsets = ClubFormWithInlineFormsets


class ClubCreate(ClubEditMixin, InlineCreateView):

    def get_form_action_url(self):
        return reverse('club_create')

    def get_bs_form_opts(self):
        return {
            'class': 'club',
            'title': 'Create sport club',
            'submit_text': 'Save sport club'
        }

    def get_success_url(self):
        action = Action(self.ff.model)
        action.do()
        return reverse('club_detail', kwargs={'club_id': self.object.pk})


class ClubUpdate(ClubEditMixin, InlineDetailView):

    format_view_title = True
    pk_url_kwarg = 'club_id'

    def get_form_action_url(self):
        return reverse('club_update', kwargs=self.kwargs)

    def get_success_url(self):
        return reverse('club_detail', kwargs={'club_id': self.object.pk})

    def get_bs_form_opts(self):
        return {
            'class': 'club',
            'title': format_html('Edit "{}"', self.object),
            'submit_text': 'Save sport club'
        }


class ClubDetail(ClubNavsMixin, InlineDetailView):

    format_view_title = True
    pk_url_kwarg = 'club_id'
    template_name = 'club_edit.htm'
    form_with_inline_formsets = ClubDisplayFormWithInlineFormsets

    def get_bs_form_opts(self):
        return {
            'class': 'club',
            'title': format_html('"{}"', self.object),
        }


class ClubList(ContextDataMixin, ClubNavsMixin, ListSortingView):

    model = Club
    template_name = 'club_list.htm'
    context_object_name = 'clubs'
    paginate_by = settings.OBJECTS_PER_PAGE
    allowed_sort_orders = '__all__'
    extra_context_data = {
        'format_local_date': format_local_date
    }
    allowed_filter_fields = {
        'category': None,
    }


class EquipmentDetail(FormDetailView):

    pk_url_kwarg = 'equipment_id'
    model = Equipment
    form_class = EquipmentDisplayForm
    format_view_title = True


class MemberDetail(FormDetailView):

    pk_url_kwarg = 'member_id'
    model = Member
    form_class = MemberDisplayForm
    format_view_title = True
