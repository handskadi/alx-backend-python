import logging
from datetime import datetime, time
from django.http import JsonResponse
from collections import defaultdict

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


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        self.start_time = time(6, 0)
        self.end_time = time(21, 0)

    def __call__(self, request):
        now = datetime.now().time()

        if not (self.start_time <= now < self.end_time):
            return JsonResponse(
                {"detail": "Access to messaging app is restricted between 9 PM and 6 AM."},
                status=403
            )

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_times = defaultdict(list)
        self.MESSAGE_LIMIT = 5
        self.TIME_WINDOW = 60

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/messages/'):
            ip = self.get_client_ip(request)
            now = time.time()

            self.ip_message_times[ip] = [t for t in self.ip_message_times[ip] if now - t < self.TIME_WINDOW]

            if len(self.ip_message_times[ip]) >= self.MESSAGE_LIMIT:
                return JsonResponse(
                    {'detail': 'Message rate limit exceeded. Please wait before sending more messages.'},
                    status=429
                )

            self.ip_message_times[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_roles = {'admin', 'moderator'}

    def __call__(self, request):
        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            user_role = getattr(user, 'role', '').lower()

            if user_role not in self.allowed_roles:
                return JsonResponse(
                    {'detail': 'You do not have permission to perform this action.'},
                    status=403
                )
        else:
            return JsonResponse(
                {'detail': 'Authentication credentials were not provided.'},
                status=403
            )

        response = self.get_response(request)
        return response