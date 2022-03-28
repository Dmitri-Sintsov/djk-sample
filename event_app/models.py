from collections import OrderedDict

from django.utils import timezone
from django.db import models
from django.db import transaction
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django_jinja_knockout.obj_dict import ObjDict
from django_jinja_knockout.tpl import format_local_date, str_dict

from djk_sample.middleware import ContextMiddleware


def user__get_str_fields(self):
    str_fields = OrderedDict([
        ('username', self.username),
    ])
    if self.first_name:
        str_fields['first_name'] = self.first_name
    if self.last_name:
        str_fields['last_name'] = self.last_name
    if self.email:
        str_fields['email'] = self.email
    return str_fields


# Monkey patch User model to support .get_str_fields(), used by ModelFormActionsView / KoGridView.
# It's not required, just serves an example and improves User interface.
User.get_str_fields = user__get_str_fields


class ActionObjDict(ObjDict):

    def can_view_field(self, field_name=None):
        return self.request_user is None or self.request_user == self.obj.performer or self.request_user.is_superuser

    def get_str_fields(self):
        return OrderedDict([
            ('performer', self.obj.performer.username),
            ('date', format_local_date(self.obj.date) if self.can_view_field() else site.empty_value_display),
            ('action_type', self.obj.get_action_type_display()),
            ('content_type', str(self.obj.content_type)),
            (
                'content_object',
                site.empty_value_display
                if self.obj.content_object is None
                else ObjDict(obj=self.obj.content_object, request_user=self.request_user).get_description()
            )
        ])


class Action(models.Model):

    TYPE_CREATED = 0
    TYPE_MODIFIED = 1
    TYPES = (
        (TYPE_CREATED, 'Created'),
        (TYPE_MODIFIED, 'Modified'),
    )

    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', verbose_name='Performer')
    date = models.DateTimeField(verbose_name='Date', db_index=True)
    action_type = models.IntegerField(choices=TYPES, verbose_name='Type of action')
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE,
        related_name='related_content', verbose_name='Related object'
    )
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name='Object link')
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'
        ordering = ('-date',)
        obj_dict_cls = ActionObjDict

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)

    # Perform action.
    @classmethod
    @transaction.atomic()
    def do(cls, obj, action_type, performer=None):
        self = cls()
        self.performer = ContextMiddleware.get_request().user if performer is None else performer
        self.date = timezone.now()
        self.action_type = action_type
        object_model = type(obj)
        self.content_type = ContentType.objects.get_for_model(object_model)
        self.object_id = obj.pk
        self.save()

    def get_str_fields(self):
        return ObjDict.from_obj(obj=self).get_str_fields()

    def __str__(self):
        str_fields = self.get_str_fields()
        return str_dict(str_fields)
