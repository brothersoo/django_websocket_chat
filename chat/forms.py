from django.forms import ModelForm

from chat.models import Room


class RoomCreateForm(ModelForm):

    class Meta:
        model = Room
        fields = ['title']

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(RoomCreateForm, self).save(**kwargs)
        instance.save()
        instance.creator = user
        instance.save()
        return instance
