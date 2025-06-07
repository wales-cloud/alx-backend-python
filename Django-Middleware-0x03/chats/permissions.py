from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants in a conversation to read/write/update/delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            # Handle Conversation objects
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()

            # Handle Message objects
            if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
                return request.user in obj.conversation.participants.all()

        return False
