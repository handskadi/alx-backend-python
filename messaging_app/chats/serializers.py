from rest_framework import serializers
from .models import user, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    full_name = serializers.SerializerMethodField()
    phone_number = serializers.CharField(source='phone_number')
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = user
        fields = ['user_id', 'email', 'first_name', 'last_name', 'full_name', 'phone_number', 'is_active', 'created']
        read_only_field = ['is_active']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def validate_email(self, value):
        if not value.endswith("@example.com"):
            raise serializers.ValidationError("Email must be on the @example.com domain.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
