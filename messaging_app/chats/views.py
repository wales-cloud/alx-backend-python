from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants (user_ids)
        Example body:
        {
            "participants": [<user_id_1>, <user_id_2>]
        }
        """
        participant_ids = request.data.get("participants", [])
        if len(participant_ids) < 2:
            return Response({"error": "A conversation needs at least 2 participants."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Example body:
        {
            "sender": "<user_id>",
            "conversation": "<conversation_id>",
            "message_body": "Hello!"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
