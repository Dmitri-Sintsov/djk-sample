from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django_jinja_knockout.forms import BootstrapModelForm, FormWithInlineFormsets, set_knockout_template
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


class EquipmentForm(BootstrapModelForm):

    class Meta:
        model = Equipment
        fields = '__all__'


class MemberForm(BootstrapModelForm):

    class Meta:
        model = Member
        fields = '__all__'


ClubEquipmentFormSet = inlineformset_factory(
    Club, Equipment, form=EquipmentForm, extra=0, min_num=1, max_num=3, can_delete=True
)
ClubEquipmentFormSet.set_knockout_template = set_knockout_template


ClubMemberFormSet = inlineformset_factory(
    Club, Member, form=MemberForm, extra=0, min_num=0, max_num=10, can_delete=True
)
ClubMemberFormSet.set_knockout_template = set_knockout_template


class ClubFormWithInlineFormsets(FormWithInlineFormsets):

    FormClass = ClubForm
    FormsetClasses = [ClubEquipmentFormSet, ClubMemberFormSet]
