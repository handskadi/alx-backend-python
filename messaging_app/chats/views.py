from django.shortcuts import render, get_list_or_404
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action 
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UsersSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter

class ConversationViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, IsParticipantOfConversation]
	queryset = Conversation.objects.all()
	serializer_class = ConversationSerializer
	filter_backends = [DjangoFilterBackend, filters.SearchFilter]
	filterset_fields = ['participants']
	search_fields = ['participants__email'] 

	def get_queryset(self):
		user = self.request.user
		return Conversation.objects.filter(participants=user)



class MessageViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, IsParticipantOfConversation]
	queryset = Message.objects.all()
	filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
	filterset_class = MessageFilter
	search_fields = ['message_body']
	serializer_class = MessageSerializer


	@action(detail=False, methods=['post'])
	def send_message(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save(sender=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	

	def get_queryset(self):
		conversation_id = self.kwargs['conversation_pk']

		user = self.request.user
		if not Conversation.objects.filter(pk=conversation_id, participants=user).exists():
			raise Http404

		return Message.objects.filter(conversation_id=conversation_id)