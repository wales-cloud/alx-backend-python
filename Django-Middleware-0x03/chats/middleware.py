from datetime import datetime, time
import logging
from django.http import JsonResponse

# Configure file-based logger
logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

# Prevent duplicate handlers
if not logger.handlers:
    logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Apply only to chat endpoints
        if request.path.startswith('/api/messages') or request.path.startswith('/api/conversations'):
            now = datetime.now().time()
            allowed_start = time(18, 0)  # 6:00 PM
            allowed_end = time(21, 0)    # 9:00 PM

            if not (allowed_start <= now <= allowed_end):
                return JsonResponse(
                    {"error": "Access to chats is restricted outside 6PM to 9PM."},
                    status=403
                )

        return self.get_response(request)
