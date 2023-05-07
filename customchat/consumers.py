from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .exceptions import ClientError
from .models import ChatRoom
from .utils import get_room_or_error, save_messages, get_exit_from_room, add_member_in_room


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.rooms = set()

    async def receive_json(self, content):
        command = content.get("command", None)
        try:
            if command == "join":
                await self.join_room(content["room"], content['user_id'])
            elif command == "leave":
                await self.leave_room(content["room"], content['user_id'])
            elif command == "send":

                await save_messages(content["message"], self.scope['user'], int(content["room"]))
                await self.send_room(content["room"], content["message"])
        except ClientError as e:
            await self.send_json({"error": e.code})

    async def disconnect(self, code):

        for room_id in list(self.rooms):
            try:
                await self.leave_room(room_id)
            except ClientError:
                pass

    async def join_room(self, room_id, user_id):

        room = await add_member_in_room(room_id, self.scope["user"])
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.join",
                "room_id": room_id,
                "username": self.scope["user"].username,
            }
        )
        self.rooms.add(room_id)
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )
        await self.send_json({
            "join": str(room.id),
            "title": str(room.id),
        })

    async def leave_room(self, room_id, user_id):

        room = await get_room_or_error(room_id, self.scope["user"])
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.leave",
                "room_id": room_id,
                "username": self.scope["user"].username,
            }
        )
        self.rooms.discard(room_id)
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )
        await self.send_json({
            "leave": str(room.id),
        })
        await get_exit_from_room(room_id, self.scope["user"])

    async def send_room(self, room_id, message):

        if room_id not in self.rooms:
            raise ClientError("ROOM_ACCESS_DENIED")
        room = await get_room_or_error(room_id, self.scope["user"])
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.message",
                "room_id": room_id,
                "username": self.scope["user"].username,
                "message": message,
            }
        )

    async def chat_join(self, event):

        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_ENTER,
                "room": event["room_id"],
                "username": event["username"],
            },
        )

    async def chat_leave(self, event):

        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_LEAVE,
                "room": event["room_id"],
                "username": event["username"],
            },
        )

    async def chat_message(self, event):

        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "room": event["room_id"],
                "username": event["username"],
                "message": event["message"],
            },
        )
