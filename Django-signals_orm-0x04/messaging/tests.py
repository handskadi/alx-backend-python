from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
import uuid
from django.utils.timezone import now

class NotificationSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="password")
        self.receiver = User.objects.create_user(username="receiver", password="password")
        self.message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")
        
    def test_notification_created_on_message(self):
        # Create a message
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")

        # Check if a notification was created
        notifications = Notification.objects.filter(user=self.receiver, message=message)
        self.assertEqual(notifications.count(), 1)

    def test_no_duplicate_notifications(self):
        # Create a message
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")

        # Ensure only one notification exists
        notifications = Notification.objects.filter(user=self.receiver, message=message)
        self.assertEqual(notifications.count(), 1)

    def test_message_edit_logs_history(self):
        # Edit the message
        self.message.content = "Updated Message"
        self.message.save()

        # Check if history was created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Original Message")

    def test_message_marked_as_edited(self):
        # Edit the message
        self.message.content = "Updated Message"
        self.message.save()

        # Check if the message is marked as edited
        self.message.refresh_from_db()
        self.assertTrue(self.message.edited)

class UserDeletionTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        # Create messages, histories, and notifications
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello")
        MessageHistory.objects.create(message=self.message, old_content="Hi")
        Notification.objects.create(user=self.user2, message=self.message, content="New message")

    def test_user_deletion_cleans_up_related_data(self):
        self.user1.delete()  # Delete user1

        # Check that related data is deleted
        self.assertEqual(Message.objects.filter(sender=self.user1).count(), 0)
        self.assertEqual(MessageHistory.objects.filter(message__sender=self.user1).count(), 0)
        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 0)

class ThreadedConversationTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        self.message1 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello")
        self.reply1 = Message.objects.create(sender=self.user2, receiver=self.user1, content="Hi!", parent_message=self.message1)
        self.reply2 = Message.objects.create(sender=self.user1, receiver=self.user2, content="How are you?", parent_message=self.reply1)

    def test_fetch_threaded_replies(self):
        replies = fetch_threaded_replies(self.message1)
        self.assertEqual(len(replies), 1)
        self.assertEqual(len(replies[0]["replies"]), 1)  # Nested reply