from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.translation import gettext_lazy as _


class users(AbstractUser):
	user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	email = models.EmailField(unique=True)
	phone_number = models.CharField(max_length=15, blank=True, null=True)
	birthdate = models.DateField(blank=True, null=True)
	first_name = models.CharField(_('first_name'),max_length=255)
	last_name = models.CharField(_('last_name'),max_length=255)
	password = models.CharField(_('password'), max_length=128)
		

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username'] 
    

class Conversation(models.Model):
	conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	participants = models.ManyToManyField(users)
	created_at = models.DateTimeField(auto_now_add=True)
    

class Message(models.Model):
	message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
	sender = models.ForeignKey(users, on_delete=models.CASCADE)
	message_body = models.TextField()
	sent_at = models.DateTimeField(auto_now_add=True)
