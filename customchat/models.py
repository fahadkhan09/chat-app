import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatRoom(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, )
    members = models.ManyToManyField(User, related_name='chat_members')

    def __str__(self):
        return 'RoomId-' + str(self.id)

    @property
    def group_name(self):
        return "room-%s" % self.id


class Messages(models.Model):
    message = models.CharField(max_length=500)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user.username)
