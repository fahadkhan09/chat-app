from django.contrib import admin
from .models import ChatRoom, Messages


# Register your models here.

class MessagesAdmin(admin.ModelAdmin):
    list_display = ['message', 'user']


admin.site.register(ChatRoom)
admin.site.register(Messages, MessagesAdmin)
