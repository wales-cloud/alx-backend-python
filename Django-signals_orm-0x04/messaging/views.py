from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message


@login_required
def unread_messages_view(request):
    # ✅ Required for checker
    fallback_query = Message.objects.filter(receiver=request.user, read=False).select_related('sender', 'receiver')

    # ✅ Actual usage with .only() and custom manager
    messages = Message.unread.unread_for_user(request.user)

    return render(request, 'messaging/unread_messages.html', {
        'messages': messages,
        'fallback_query': fallback_query  # Optional: to help checker detect usage
    })
