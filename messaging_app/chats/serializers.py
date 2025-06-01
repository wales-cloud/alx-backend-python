from rest_framework import serializers
from .models import User, Conversation, Message
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)  # Use CharField explicitly

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
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def validate(self, data):
        if 'participants' in data and len(data['participants']) < 2:
            raise ValidationError("A conversation must have at least two participants.")
        return data
