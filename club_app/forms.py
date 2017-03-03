from django.utils.html import format_html
from django import forms
from django.forms.models import BaseInlineFormSet

from django_jinja_knockout.widgets import DisplayText, ForeignKeyGridWidget
from django_jinja_knockout.forms import (
    BootstrapModelForm, WidgetInstancesMixin, DisplayModelMetaclass,
    FormWithInlineFormsets, ko_inlineformset_factory
)
from django_jinja_knockout.viewmodels import to_json

from djk_sample.middleware import ContextMiddleware
from event_app.models import Action
from .models import Profile, Manufacturer, Club, Equipment, Member


class ProfileForm(BootstrapModelForm):

    class Meta:
        model = Profile
        fields = '__all__'


class ManufacturerForm(BootstrapModelForm):

    class Meta:
        model = Manufacturer
        fields = '__all__'


class ClubForm(BootstrapModelForm):

    class Meta:
        model = Club
        fields = '__all__'
        exclude = ('last_update',)
        widgets = {
            'category': forms.RadioSelect()
        }

    def save(self, commit=True):
        action_type = Action.TYPE_CREATED if self.instance.pk is None else Action.TYPE_MODIFIED
        obj = super().save(commit=commit)
        if self.has_changed():
            ContextMiddleware().add_action(obj, action_type)
        return obj


class ClubDisplayForm(BootstrapModelForm, metaclass=DisplayModelMetaclass):

    class Meta(ClubForm.Meta):
        widgets = {
            'category': DisplayText()
        }


class EquipmentForm(BootstrapModelForm):

    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'manufacturer': ForeignKeyGridWidget(model=Manufacturer, grid_options={
                'pageRoute': 'manufacturer_fk_widget_grid',
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
class EquipmentDisplayForm(WidgetInstancesMixin, BootstrapModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = Equipment
        fields = '__all__'


class ClubEquipmentForm(EquipmentForm):

    class Meta(EquipmentForm.Meta):
        widgets = {
            'club': forms.HiddenInput(),
            'manufacturer': ForeignKeyGridWidget(model=Manufacturer, grid_options={
                'pageRoute': 'manufacturer_fk_widget_grid',
            }),
            'category': forms.RadioSelect()
        }


class MemberForm(BootstrapModelForm):

    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'profile': ForeignKeyGridWidget(model=Profile, grid_options={
                'pageRoute': 'profile_fk_widget_grid',
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


class MemberFormNoRelations(MemberForm):

    class Meta(MemberForm.Meta):
        exclude = ('club', 'profile')


class MemberDisplayForm(WidgetInstancesMixin, BootstrapModelForm, metaclass=DisplayModelMetaclass):

    class Meta:

        def get_note(self, value):
            # self.instance.accepted_license.version
            if self.instance is None or self.instance.note.strip() == '':
                return 'No note'
            return format_html(
                '<button class="btn btn-info dialog-button" data-options=\'{}\'>Read</button>',
                to_json({
                    'title': '<b>Note for </b> <i>{}</i>'.format(self.instance.profile),
                    'message': format_html('<div class="preformatted">{}</div>', self.instance.note),
                    'method': 'alert'
                })
            )

        model = Member
        fields = '__all__'
        widgets = {
            'note': DisplayText(get_text_method=get_note)
        }


ClubEquipmentFormSet = ko_inlineformset_factory(
    Club, Equipment, form=EquipmentForm, extra=0, min_num=1, max_num=5, can_delete=True
)
ClubDisplayEquipmentFormSet = ko_inlineformset_factory(
    Club, Equipment, form=EquipmentDisplayForm
)


class ClubMemberFormSetCls(BaseInlineFormSet):

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


class ClubDisplayFormWithInlineFormsets(FormWithInlineFormsets):

    FormClass = ClubDisplayForm
    FormsetClasses = [ClubDisplayEquipmentFormSet, ClubDisplayMemberFormSet]
