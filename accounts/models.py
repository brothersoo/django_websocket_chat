from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)
    nickname = models.CharField(_('nickname'), max_length=50, unique=True, null=False)

    class UserStatus(models.TextChoices):
        ACTIVE: tuple = 'ACT', _('Active')
        BANNED: tuple = 'BAN', _('Banned')
        QUIT: tuple = 'QIT', _('Quit')

    status = models.CharField(_('status'), choices=UserStatus.choices, max_length=3, default=UserStatus.ACTIVE)

    class Meta(AbstractUser.Meta):
        verbose_name = _('dc_user')
        verbose_name_plural = _('dc_users')
        db_table = 'dc_user'

