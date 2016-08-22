from collections import OrderedDict

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django_jinja_knockout.tpl import format_local_date
from django_jinja_knockout.utils.sdv import join_dict_values


class Action(models.Model):

    TYPE_CREATED = 0
    TYPE_MODIFIED = 1
    TYPES = (
        (TYPE_CREATED, 'Created'),
        (TYPE_MODIFIED, 'Modified'),
    )

    performer = models.ForeignKey(User, related_name='+', verbose_name='Performer')
    date = models.DateTimeField(verbose_name='Date', db_index=True)
    type = models.IntegerField(choices=TYPES, verbose_name='Type of action')
    content_type = models.ForeignKey(ContentType, related_name='related_content', blank=True, null=True,
                                     verbose_name='Related object')
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name='Object link')
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'
        ordering = ('-date',)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)

    def get_str_fields(self):
        return OrderedDict([
            ('performer', self.performer.username),
            ('date', format_local_date(self.date)),
            ('type', self.get_type_display()),
            ('content_type', str(self.content_type)),
            (
                'content_object',
                self.content_object.get_str_fields() if hasattr(self.content_object, 'get_str_fields') else str(self.content_object)
            )
        ])

    def __str__(self):
        str_fields = self.get_str_fields()
        if isinstance(str_fields['content_object'], dict):
            join_dict_values(' / ', str_fields, ['content_object'])
        return ' › '.join(str_fields.values())
