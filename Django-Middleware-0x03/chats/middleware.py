from datetime import datetime, time
from time import time as timestamp
import logging
from django.http import JsonResponse

# Configure file-based logger
logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

# Avoid duplicate handlers in dev mode
if not logger.handlers:
    logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_history = {}  # {ip: [timestamps]}

    def __call__(self, request):
        if request.path.startswith('/api/messages') and request.method == "POST":
            ip = self.get_client_ip(request)
            now = timestamp()
            timestamps = self.ip_history.get(ip, [])
            # Keep only timestamps from the last 60 seconds
            timestamps = [t for t in timestamps if now - t < 60]

            if len(timestamps) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded: Only 5 messages per minute allowed."},
                    status=403
                )

            timestamps.append(now)
            self.ip_history[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        return request.META.get('REMOTE_ADDR', '')


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = ['/api/messages', '/api/conversations']
        if any(request.path.startswith(p) for p in restricted_paths):
            if request.user.is_authenticated:
                role = getattr(request.user, 'role', None)
                if role not in ['admin', 'moderator']:
                    return JsonResponse(
                        {"error": "You do not have permission to perform this action."},
                        status=403
                    )
            else:
                return JsonResponse(
                    {"error": "Authentication required."},
                    status=403
                )

        return self.get_response(request)
