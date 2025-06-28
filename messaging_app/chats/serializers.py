from rest_framework import serializers
from .models import users, Conversation, Message
from rest_framework.serializers import ValidationError

class UsersSerializer(serializers.ModelSerializer):

	full_name = serializers.SerializerMethodField()

	class Meta:
		model = users
		fields = ['user_id', 'email', 'first_name', 'last_name', 'full_name', 'password']

		extra_kwargs = {
			'password' : {'write_only': True}
		}

	
	def get_full_name(self, obj):
		return f"{obj.first_name} {obj.last_name}"
	
	def validate_password(self, value):

		if len(value) < 8:
			raise serializers.ValidationError("Password must be at least 8 chars long")
		return value
	
	def create(self, validated_data):
		user = users.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
		)
		return user


class ConversationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Conversation
		# serializers.CharField
		fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = "__all__"