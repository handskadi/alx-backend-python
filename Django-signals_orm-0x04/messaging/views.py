from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@cache_page(60)
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related(
        'sender', 'receiver'
    ).order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@require_http_methods(["DELETE"])
@login_required
def delete_user(request):
    user = request.user
    username = user.username
    user.delete()
    return JsonResponse({"message": f"User '{username}' and related data deleted."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages_view(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user).only('id', 'content', 'timestamp', 'sender')
    serializer = MessageSerializer(unread_messages, many=True)
    return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.filter().select_related(
        'sender', 'receiver', 'edited_by', 'parent_message'
    ).prefetch_related('replies')
    serializer_class = MessageSerializer

    def perform_create(self, request, serializer):
        sender=request.user
        serializer.save(sender)

    @action(detail=True, methods=['get'], url_path='thread')
    def get_thread(self, request, pk=None):
        message = get_object_or_404(Message, pk=pk)
        thread_replies = message.get_thread()
        serializer = self.get_serializer(thread_replies, many=True)
        return Response(serializer.data)