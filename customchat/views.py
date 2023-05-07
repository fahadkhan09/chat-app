import json

from account.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
import requests

from customchat.models import ChatRoom, Messages
from customchat.serializer import MessageSerializer, ChatRoomSerializer


@login_required(login_url='/account/login/')
def CreateChatRoom(request):
    rooms = ChatRoom.objects.create(owner=request.user)
    return HttpResponseRedirect('chat_room/' + str(rooms.id))


@login_required(login_url='/account/login/')
def CustomChatRoom(request, slug):
    try:
        room = ChatRoom.objects.filter(id=slug)
    except:
        room = None
    message = {'status': 'active'}
    if len(room) > 0:
        message['rooms'] = room
        old_data = Messages.objects.filter(chat_room_id=int(slug))
        previous_msg = []
        for msg in old_data:
            previous_msg.append({'message': msg.message, 'username': msg.user.username, 'msg_type': 0, 'room': slug,
                                 'created_at': msg.created_at.strftime("%m/%d/%Y")})
        message['room_id'] = room.first().id
        message['previous_msg'] = json.dumps(previous_msg)
    else:
        message = {'status': 'inactive'}

    return render(request, "chat_room.html", message)


@login_required(login_url='/account/login/')
def index(request):
    chat_room = ChatRoom.objects.filter(members=request.user)
    context = {'chat_room': chat_room}
    return render(request, 'index.html', context)


class LoginViewSet(ViewSet):
    serializer_class = AuthTokenSerializer

    def create(self, request):
        # email = request.data.get('username').lower()
        # password = request.data.get('password')
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        return self.queryset.filter(members=self.request.user)


class MessagesViewSet(ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        param = self.request.query_params.get('chatroom')
        if param:
            self.queryset.filter(chat_room_id=param, user=self.request.user)
        else:
            self.queryset.filter(user=self.request.user)
