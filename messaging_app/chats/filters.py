import django_filters
from django_filters.rest_framework import FilterSet, DateTimeFilter
from .models import Message

class MessageFilter(FilterSet):
    start_date = DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date = DateTimeFilter(field_name="created_at", lookup_expr='lte')
    sender = django_filters.NumberFilter(field_name='sender__id')
    conversation = django_filters.NumberFilter(field_name='conversation__id')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'start_date', 'end_date']
