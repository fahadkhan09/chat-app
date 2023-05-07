from channels.db import database_sync_to_async

from .models import ChatRoom, Messages


@database_sync_to_async
def get_room_or_error(room_id, user):
    try:
        room = ChatRoom.objects.get(pk=room_id, members=user.id)
    except ChatRoom.DoesNotExist:
        room = None

    return room


@database_sync_to_async
def add_member_in_room(room_id, user):
    try:
        room = ChatRoom.objects.get(pk=room_id)
        room.members.add(user)
        room.save()
    except ChatRoom.DoesNotExist:
        room = None

    return room


@database_sync_to_async
def get_exit_from_room(room_id, user):
    try:
        room = ChatRoom.objects.get(pk=room_id)
        room.members.remove(user)
        room.save()
    except ChatRoom.DoesNotExist:
        room = None

    return room


@database_sync_to_async
def save_messages(message, user, chat_room):
    return Messages.objects.create(message=message, user=user, chat_room_id=chat_room)
