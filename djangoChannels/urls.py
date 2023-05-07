"""djangoChannels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from customchat.views import index, CreateChatRoom, CustomChatRoom, MessagesViewSet, LoginViewSet, ChatRoomViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('rest_login/', LoginViewSet.as_view({'get': 'json'}), name='rest_login'),
    path('rest_chatroom/', ChatRoomViewSet.as_view({'get': 'json'}), name='rest_chatroom'),
    path('account/', include("account.urls")),
    path('create_room', CreateChatRoom, name='create_room'),
    path('chat_room/<slug:slug>', CustomChatRoom, name='chat_room'),
    path('messages/', MessagesViewSet.as_view({'get': 'json'}), name='messages')
]
