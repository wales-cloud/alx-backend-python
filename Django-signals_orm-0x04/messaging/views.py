# messaging/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
@login_required
def delete_user(request):
    request.user.delete()
    return redirect('home')  # adjust this to your landing page or login screen
