from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=True, unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)
    nickname = models.CharField(_('nickname'), max_length=50, unique=True, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class UserStatus(models.TextChoices):
        ACTIVE: tuple = 'ACT', _('Active')
        BANNED: tuple = 'BAN', _('Banned')
        QUIT: tuple = 'QIT', _('Quit')

    status = models.CharField(_('status'), choices=UserStatus.choices, max_length=3, default=UserStatus.ACTIVE)

    class Meta(AbstractUser.Meta):
        verbose_name = _('dc_user')
        verbose_name_plural = _('dc_users')
        db_table = 'dc_user'

    @classmethod
    def get_user_by_email(cls, email: str):
        return cls.objects.get(email=email)

    @classmethod
    def get_user_by_nickname(cls, nickname: str):
        return cls.objects.get(nickname=nickname)
