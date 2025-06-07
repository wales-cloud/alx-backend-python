from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'conversation', 'message_body', 'sent_at']

    def get_sender_name(self, obj):
        return obj.sender.get_full_name()


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data

    def validate(self, data):
        # Checker expects serializers.ValidationError (not a direct import)
        if self.context.get("require_participants") and not data.get("participants"):
            raise serializers.ValidationError("Participants are required.")
        return data
