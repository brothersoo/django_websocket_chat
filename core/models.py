from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):

    objects = models.Manager()

    class Meta:
        abstract = True


class TimeStampedModel(BaseModel):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True

