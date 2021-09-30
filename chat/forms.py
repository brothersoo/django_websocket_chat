from django.db import transaction
from django.forms import ModelForm

from chat.models import Room


class RoomCreateForm(ModelForm):

    class Meta:
        model = Room
        fields = ['title']

    def save(self, **kwargs):
        self.instance.creator = kwargs.pop('user')
        instance: Room = super(RoomCreateForm, self).save(**kwargs)
        instance.save()
        return instance

