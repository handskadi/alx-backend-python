from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Filters unread messages for the specified user.
        """
        return self.filter(receiver=user, read=False).only("id", "sender", "content", "timestamp")


class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )  # Self-referential FK for threaded replies
    edited = models.BooleanField(default=False)  # Track if the message has been edited
    edited_at = models.DateTimeField(null=True, blank=True)  # When the message was edited
    edited_by = models.ForeignKey(User, related_name="edited_messages", on_delete=models.SET_NULL, null=True, blank=True)

    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

    class Meta:
        ordering = ["-timestamp"] # Show the latest messages first - Ensures chronological order

class Notification(models.Model):
    notification_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message_id}"

class MessageHistory(models.Model):
    history_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    timestamp = models.DateTimeField(default=now)  # When the edit occurred

    def __str__(self):
        return f"History for Message {self.message.message_id}"