from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'parent_message', 'replies']

    def get_replies(self, obj):
        return MessageSerializer(obj.replies.all(), many=True).data