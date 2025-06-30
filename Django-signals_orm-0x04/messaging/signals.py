from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.db.models.signals import pre_save
from django.utils.timezone import now

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Check if the message already exists (not being created)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # Check if the content is changing
                # Log the old content in the MessageHistory model
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                # Mark the message as edited
                instance.edited = True
                instance.edited_at = now()
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def clean_up_related_data(sender, instance, **kwargs):
    # Delete all messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete all message histories related to the user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()

    # Delete all notifications related to the user
    Notification.objects.filter(user=instance).delete()