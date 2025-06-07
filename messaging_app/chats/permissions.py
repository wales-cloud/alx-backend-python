from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own data
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users who are participants of a conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If the object is a conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # If the object is a message with a conversation
        if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            return request.user in obj.conversation.participants.all()

        return False
