from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from django_jinja_knockout.middleware import ContextMiddleware

from .models import Action


class ObjectAction:

    object_model = None
    action = Action

    def __init__(self, obj, performer=None):
        self.action = None
        self.object = obj
        self.performer = ContextMiddleware.get_request() if performer is None else performer
        self.object_model = type(obj)
        if self.__class__.object_model is not None and \
                self.object_model is not self.__class__.object_model:
            raise ValueError('Content object {0} has unexpected type: {1}'.format(obj, self.object_model))
        self.content_type = ContentType.objects.get_for_model(self.object_model)

    # Perform action.
    @transaction.atomic()
    def do(self, action_type):
        # Create action.
        self.action = self.__class__.action()
        self.action.performer = self.performer
        self.action.date = timezone.now()
        self.action.type = action_type
        self.action.content_type = self.content_type
        self.action.object_id = self.object.pk
        self.action.save()
