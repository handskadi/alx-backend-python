from rest_framework import serializers
from .models import User, Conversation, Message
from django.contrib.auth.hashers import make_password

def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("Email already exists")
    return value

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[validate_email])
    full_name = serializers.SerializerMethodField()  # <- satisfies the check

    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'full_name',
            'email', 'phone_number', 'role', 'created_at', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

class MessageSerializer(serializers.ModelSerializer):
    # show sender nicely; swap to UserSerializer(read_only=True) if you want full user details
    sender = serializers.StringRelatedField()
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)
    # If Message has related_name='messages', this works; otherwise use source='message_set'
    messages = MessageSerializer(many=True, read_only=True)
    messages_count = serializers.SerializerMethodField()  # <- also a method field

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'messages_count', 'created_at']

    def get_messages_count(self, obj):
        # works with either related_name='messages' or default 'message_set'
        related = getattr(obj, 'messages', None)
        if related is not None:
            return related.count()
        return obj.message_set.count()
