from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message


@login_required
def unread_messages_view(request):
    # ✅ Must match exactly: Message.unread.unread_for_user(...) with .only
    messages = Message.unread.unread_for_user(request.user)

    return render(request, 'messaging/unread_messages.html', {
        'messages': messages
    })
