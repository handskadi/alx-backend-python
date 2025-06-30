from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

User = get_user_model()

@require_http_methods(["DELETE"])
@login_required
def delete_user(request):
    user = request.user
    username = user.username
    user.delete()
    return JsonResponse({"message": f"User '{username}' and related data deleted."})