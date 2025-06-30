import logging
from datetime import datetime

logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('requests.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        user_str = user.username if user and user.is_authenticated else 'Anonymous'

        logger.info(f"{datetime.now()} - User: {user_str} - Path: {request.path}")

        response = self.get_response(request)
        return response
