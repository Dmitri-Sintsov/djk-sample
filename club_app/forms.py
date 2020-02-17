from django.utils.html import format_html
from django import forms
from django.forms.models import BaseInlineFormSet

from django_jinja_knockout.widgets import DisplayText, ForeignKeyGridWidget, PrefillWidget, MultipleKeyGridWidget
from django_jinja_knockout.forms import (
    RendererModelForm, WidgetInstancesMixin, DisplayModelMetaclass,
    FormWithInlineFormsets, ko_inlineformset_factory
)
from django_jinja_knockout.query import ListQuerySet
from django_jinja_knockout.tpl import format_html_attrs

from djk_sample.middleware import ContextMiddleware
from event_app.models import Action
from .models import Profile, Manufacturer, Club, Equipment, Member, Tag


class ProfileForm(RendererModelForm):

    class Meta:
        model = Profile
        fields = '__all__'


class ManufacturerForm(RendererModelForm):

    class Meta:
        model = Manufacturer
        fields = '__all__'


class ClubForm(RendererModelForm):

    def add_tag_set_checkbox(self):
        self.fields['tag_set'] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            queryset=Tag.objects.all(),
            required=False,
        )
        if self.instance.pk is not None:
            self.fields['tag_set'].initial = self.instance.tag_set.values_list('id', flat=True)

    def add_tag_set_fk_grid(self):
        # https://kite.com/python/docs/django.forms.ModelMultipleChoiceField
        # value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
        self.fields['tag_set'] = forms.ModelMultipleChoiceField(
            widget=MultipleKeyGridWidget(grid_options={
                'pageRoute': 'tag_fk_widget',
            }),
            queryset=Tag.objects.all(),
            required=False,
        )
        if self.instance.pk is not None:
            self.fields['tag_set'].initial = self.instance.tag_set.values_list('id', flat=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_tag_set_fk_grid()
        # self.add_tag_set_checkbox()

    class Meta(RendererModelForm.Meta):
        model = Club
        fields = '__all__'
        exclude = ('last_update',)
        widgets = {
            'category': forms.RadioSelect()
        }

    def save(self, commit=True):
        action_type = Action.TYPE_CREATED if self.instance.pk is None else Action.TYPE_MODIFIED
        obj = super().save(commit=commit)
        # Save reverse many to many 'tag_set' relation.
        obj.tag_set.set(self.cleaned_data['tag_set'])
        if self.has_changed():
            ContextMiddleware().add_action(obj, action_type)
        return obj


class ClubDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta(ClubForm.Meta):
        widgets = {
            'category': DisplayText()
        }


class EquipmentForm(RendererModelForm):

    inline_template = 'inline_equipment_form.htm'

    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'manufacturer': ForeignKeyGridWidget(model=Manufacturer, grid_options={
                'pageRoute': 'manufacturer_fk_widget',
            }),
            'category': forms.RadioSelect()
        }

    def save(self, commit=True):
        action_type = Action.TYPE_CREATED if self.instance.pk is None else Action.TYPE_MODIFIED
        obj = super().save(commit=commit)
        if self.has_changed():
            ContextMiddleware().add_action(obj, action_type)
        return obj


# WidgetInstancesMixin is used to automatically render club via self.club.instance.get_str_fields().
class EquipmentDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = Equipment
        fields = '__all__'


class ClubEquipmentForm(EquipmentForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['club'].widget = forms.HiddenInput()


class MemberForm(RendererModelForm):

    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'profile': ForeignKeyGridWidget(model=Profile, grid_options={
                'pageRoute': 'profile_fk_widget',
                'dialogOptions': {'size': 'size-wide'},
            }),
            'club': ForeignKeyGridWidget(model=Club, grid_options={
                'pageRoute': 'club_grid_simple',
            }),
            'plays': forms.RadioSelect(),
            'role': forms.RadioSelect()
        }

    def clean(self):
        super().clean()
        role = self.cleaned_data.get('role')
        club = self.cleaned_data.get('club')
        if role != Member.ROLE_MEMBER:
            current_member = Member.objects.filter(club=club, role=role).first()
            if current_member is not None and current_member != self.instance:
                self.add_error('role', 'Non-member roles should be unique')

    def save(self, commit=True):
        action_type = Action.TYPE_CREATED if self.instance.pk is None else Action.TYPE_MODIFIED
        obj = super().save(commit=commit)
        if self.has_changed():
            ContextMiddleware().add_action(obj, action_type)
        return obj


class TagForm(RendererModelForm):

    class Meta:
        model = Tag
        fields = ['name']


class MemberDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:

        def get_note(self, value):
            # self.instance.accepted_license.version
            if self.instance is None or self.instance.note.strip() == '':
                # Do not display empty row.
                self.skip_output = True
                return None
            return format_html_attrs(
                '<button {attrs}>Read</button>',
                attrs={
                    'class': 'component btn btn-info',
                    'data-component-class': 'App.Dialog',
                    'data-event': 'click',
                    'data-component-options': {
                        'title': '<b>Note for </b> <i>{}</i>'.format(self.instance.profile),
                        'message': format_html('<div class="preformatted">{}</div>', self.instance.note),
                        'method': 'alert'
                    }
                }
            )

        model = Member
        fields = '__all__'
        widgets = {
            'note': DisplayText(get_text_method=get_note)
        }


ClubEquipmentFormSet = ko_inlineformset_factory(
    Club, Equipment, form=EquipmentForm, extra=0, min_num=1, max_num=5, can_delete=True
)
ClubEquipmentFormSet.template = 'club_equipment_formset.htm'
ClubDisplayEquipmentFormSet = ko_inlineformset_factory(
    Club, Equipment, form=EquipmentDisplayForm
)


class ClubMemberFormSetCls(BaseInlineFormSet):

    def set_request(self, request):
        self.request = request
        # Not a nice way to load widget data, but formset factories are a bit too inflexible.
        # todo: Load with AJAX calls can be implemented in cleaner way.
        self.related_members_qs = ListQuerySet(
            Member.objects.filter(
                club__id=request.resolver_match.kwargs.get('club_id', None)
            )
        )

    def add_fields(self, form, index):
        super().add_fields(form, index)
        if isinstance(form, MemberForm) and self.related_members_qs.count() > 1:
            form.fields['note'].widget = PrefillWidget(
                data_widget=form.fields['note'].widget,
                choices=self.related_members_qs.prefill_choices('note')
            )

    def clean(self):
        if any(self.errors):
            return
        roles = []
        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                # Do not validate deleted forms.
                continue
            # Warning! May be None, thus dict.get() is used.
            role = form.cleaned_data.get('role')
            if role != Member.ROLE_MEMBER:
                if role in roles:
                    form.add_error('role', 'Non-member roles should be unique')
                    # raise forms.ValidationError(msg)
                else:
                    roles.append(role)


ClubMemberFormSet = ko_inlineformset_factory(
    Club, Member, form=MemberForm, formset=ClubMemberFormSetCls, extra=0, min_num=0, max_num=10, can_delete=True
)
ClubDisplayMemberFormSet = ko_inlineformset_factory(
    Club, Member, form=MemberDisplayForm
)


class ClubFormWithInlineFormsets(FormWithInlineFormsets):

    FormClass = ClubForm
    FormsetClasses = [ClubEquipmentFormSet, ClubMemberFormSet]
    prefix = 'test'


class ClubDisplayFormWithInlineFormsets(FormWithInlineFormsets):

    FormClass = ClubDisplayForm
    FormsetClasses = [ClubDisplayEquipmentFormSet, ClubDisplayMemberFormSet]
