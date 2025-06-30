from django.contrib import admin
from .models import Message, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "content", "edited", "timestamp")
    search_fields = ("sender__username", "receiver__username", "content")
    list_filter = ("edited", "timestamp",)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "is_read", "timestamp")
    search_fields = ("user__username", "message__content")
    list_filter = ("is_read", "timestamp")

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("message", "old_content", "timestamp")
    search_fields = ("message__content",)
    list_filter = ("timestamp",)