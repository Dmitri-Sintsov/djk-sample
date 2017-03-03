from django.core.urlresolvers import reverse
from django.utils.html import format_html, mark_safe
from django.shortcuts import render

from django_jinja_knockout.tpl import format_local_date
from django_jinja_knockout.views import (
    FormDetailView, InlineCreateView, InlineDetailView, ListSortingView, BsTabsMixin, ContextDataMixin
)
from django_jinja_knockout.viewmodels import to_json

from djk_sample.middleware import ContextMiddleware

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
        return reverse('club_detail', kwargs={'club_id': self.object.pk})


class ClubCreateDTL(ClubCreate):

    template_name = 'club_create.html'


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
    allowed_sort_orders = '__all__'
    extra_context_data = {
        'format_local_date': format_local_date
    }
    allowed_filter_fields = {
        'category': None,
    }
    grid_fields = [
        'title',
        'category',
        'foundation_date',
    ]

    def get_title_links(self, obj):
        links = [format_html(
            '<div><a href="{}">{}</a></div>',
            reverse('club_detail', kwargs={'club_id': obj.pk}),
            obj.title
        )]
        if ContextMiddleware.get_request().user.is_authenticated():
            links.append(format_html(
                '<a href="{}"><span class="glyphicon glyphicon-edit"></span></a>',
                reverse('club_update', kwargs={'club_id': obj.pk})
            ))
            links.append(format_html(
                '<a href="{}"><span class="glyphicon glyphicon-user"></span></a>',
                reverse('club_member_grid', kwargs={'action': '', 'club_id': obj.pk})
            ))
        return links

    def get_display_value(self, obj, field):
        if field == 'title':
            links = self.get_title_links(obj)
            return mark_safe(''.join(links))
        else:
            return super().get_display_value(obj, field)


class ClubListWithComponent(ClubList):

    client_routes = [
        'club_member_grid',
        'profile_fk_widget_grid',
    ]
    template_name = 'club_list_with_component.htm'

    def get_title_links(self, obj):
        links = super().get_title_links(obj)
        links.append(format_html(
            '<button class="component" data-event="click" data-component-options="{}">'
            '<span class="glyphicon glyphicon-user"></span>See inline'
            '</button>',
            to_json({
                'classPath': 'App.GridDialog',
                'filterOptions': {
                    'pageRoute': 'club_member_grid',
                    'pageRouteKwargs': {'club_id': obj.pk},
                    'fkGridOptions': {
                        'profile': 'profile_fk_widget_grid',
                    }
                }
            })
        ))
        return links


class ClubListDTL(ClubList):
    template_name = 'club_list.html'


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
