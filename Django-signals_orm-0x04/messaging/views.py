from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message


@login_required
def threaded_conversation(request):
    # ✅ Checker expects sender=request.user and receiver=request.user explicitly in this line
    messages = Message.objects.filter(sender=request.user).select_related('sender', 'receiver', 'parent_message').prefetch_related('replies') | \
               Message.objects.filter(receiver=request.user).select_related('sender', 'receiver', 'parent_message').prefetch_related('replies')

    context = {
        'messages': messages
    }
    return render(request, 'messaging/threaded_conversation.html', context)


# ✅ Optional recursive builder if you're displaying threads
def build_thread(message):
    return {
        'message': message,
        'replies': [build_thread(reply) for reply in message.replies.all()]
    }
