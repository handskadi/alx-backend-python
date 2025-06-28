import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    
    class Meta:
        model = Message
        fields = {
            "sent_at" : ["lt", "gt"],
            "sender" : ['exact']
        }
