from django.contrib.auth import get_user_model
from django.db import transaction

from chat.models import Room, Participate


User = get_user_model()


@transaction.atomic()
def participate(room: Room, user: User) -> None:
    if room.creator == user:
        return

    try:
        participation: Participate = room.participate_set.get(user=user)
        if participation.status is Participate.ParticipateStatus.LEFT:
            participation.status = Participate.ParticipateStatus.PARTICIPATING
    except Participate.DoesNotExist:
        room.users.add(user)
