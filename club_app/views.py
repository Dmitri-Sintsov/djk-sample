from django.utils.html import format_html, mark_safe
from django.shortcuts import render

from django_jinja_knockout.utils.sdv import call_prop
from django_jinja_knockout.tpl import format_local_date, reverse, format_html_attrs, add_css_classes_to_dict
from django_jinja_knockout.views import (
    djk_get_decorator, BsTabsMixin, NavsList,
    FormDetailView, InlineCreateView, InlineDetailView, InlineCrudView, ListSortingView
)

from djk_sample.middleware import ContextMiddleware

from .models import Club, Equipment, Member
from .forms import EquipmentDisplayForm, MemberDisplayForm, ClubFormWithInlineFormsets, ClubDisplayFormWithInlineFormsets


@djk_get_decorator(view_title='Decorated main page title')
def main_page(request, **kwargs):
    return render(request, 'main.htm')


class ClubNavsMixin(BsTabsMixin):

    def get_main_navs(self, object_id=None):
        main_navs = NavsList([
            {'url': reverse('club_list'), 'text': 'List of clubs'},
            {'url': reverse('club_create'), 'text': 'Create new club'}
        ])
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

    client_routes = {
        'manufacturer_fk_widget_grid',
        'profile_fk_widget_grid'
    }
    template_name = 'club_edit.htm'
    form_with_inline_formsets = ClubFormWithInlineFormsets


class ClubCreate(ClubEditMixin, InlineCreateView):

    view_title = 'Add new club'

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


class ClubUpdate(ClubEditMixin, InlineCrudView):

    format_view_title = True
    pk_url_kwarg = 'club_id'

    def get_success_url(self):
        return reverse('club_detail', kwargs={'club_id': self.object.pk})

    def get_bs_form_opts(self):
        return {
            'class': 'club',
            'title': format_html('Edit "{}"', self.object),
            'submit_text': 'Save sport club'
        }


class ClubDetail(ClubNavsMixin, InlineDetailView):

    view_title = 'Detail for "{}"'
    format_view_title = True
    pk_url_kwarg = 'club_id'
    template_name = 'club_edit.htm'
    form_with_inline_formsets = ClubDisplayFormWithInlineFormsets

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data

    def get_bs_form_opts(self):
        return {
            'class': 'club',
            'title': format_html('"{}"', self.object),
        }


class ClubList(ClubNavsMixin, ListSortingView):

    model = Club
    allowed_sort_orders = '__all__'
    extra_context = {
        'format_local_date': format_local_date
    }
    highlight_mode = 'linearRows'
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
        # is_authenticated is not callable in Django 2.0.
        if call_prop(self.request.user.is_authenticated):
            links.append(format_html(
                '<a href="{}"><span class="iconui iconui-edit"></span></a>',
                reverse('club_update', kwargs={'club_id': obj.pk})
            ))
            links.append(format_html(
                '<a href="{}"><span class="iconui iconui-user"></span></a>',
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

    client_routes = {
        'club_member_grid',
        'profile_fk_widget_grid',
    }
    template_name = 'club_list_with_component.htm'
    highlight_mode = 'cycleColumns'

    def get_table_attrs(self):
        table_attrs = super().get_table_attrs()
        add_css_classes_to_dict(table_attrs, 'rows-strong-border')
        return table_attrs

    def get_title_links(self, obj):
        links = super().get_title_links(obj)
        links.append(format_html_attrs(
            ' <button {attrs}>'
            '<span class="iconui iconui-user"></span> See inline'
            '</button>',
            attrs={
                'class': 'component btn btn-sm btn-light',
                'data-event': 'click',
                'data-component-class': 'App.GridDialog',
                'data-component-options': {
                    'filterOptions': {
                        'pageRoute': 'club_member_grid',
                        'pageRouteKwargs': {'club_id': obj.pk},
                        'fkGridOptions': {
                            'profile': 'profile_fk_widget_grid',
                        }
                    }
                }
            }
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
