from datetime import datetime
import logging

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
