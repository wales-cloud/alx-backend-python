from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message


@login_required
def unread_messages_view(request):
    # ✅ Use the custom manager to get unread messages
    messages = Message.unread.for_user(request.user)

    return render(request, 'messaging/unread_messages.html', {
        'messages': messages
    })
