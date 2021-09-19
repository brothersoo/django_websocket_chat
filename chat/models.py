from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel
from django_websocket_chat.settings import AUTH_USER_MODEL


class Room(TimeStampedModel):
    title = models.CharField(_('title'), max_length=50, null=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class RoomStatus(models.TextChoices):
        ACTIVE: tuple = 'ACT', _('Active')
        REMOVED: tuple = 'RMV', _('Removed')
        HIDDEN: tuple = 'HID', _('Hidden')

    status = models.CharField(_('status'), choices=RoomStatus.choices, max_length=3, default=RoomStatus.ACTIVE)

    class Meta:
        verbose_name = _('dc_room')
        verbose_name_plural = _('dc_rooms')
        db_table = _('dc_room')


class RoomsUsers(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = _('dc_roomsusers')
        db_table = _('dc_roomsusers')

