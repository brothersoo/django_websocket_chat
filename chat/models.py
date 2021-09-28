from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel
from django_websocket_chat.settings import AUTH_USER_MODEL


class Room(TimeStampedModel):
    title = models.CharField(_('title'), max_length=50, null=False)
    users = models.ManyToManyField(AUTH_USER_MODEL, through='Participate', related_name='participating_rooms')
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='created_room', null=True)

    class RoomStatus(models.TextChoices):
        ACTIVE: tuple = 'ACT', _('Active')
        REMOVED: tuple = 'RMV', _('Removed')
        HIDDEN: tuple = 'HID', _('Hidden')

    status = models.CharField(_('status'), choices=RoomStatus.choices, max_length=3, default=RoomStatus.ACTIVE)

    class Meta:
        verbose_name = _('dc_room')
        verbose_name_plural = _('dc_rooms')
        db_table = _('dc_room')


class Participate(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    class ParticipateStatus(models.TextChoices):
        PARTICIPATING: tuple = 'PRT', _('Participating')
        LEFT: tuple = 'LFT', _('Left')

    status = models.CharField(_('status'), choices=ParticipateStatus.choices, max_length=3,
                              default=ParticipateStatus.PARTICIPATING)

    class Meta:
        verbose_name = _('dc_participate')
        db_table = _('dc_participate')

