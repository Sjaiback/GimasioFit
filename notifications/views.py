import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import NotificationTemplate
from .services import queue_membership_expiration_reminders, send_pending_email_notifications


def _json_body(request):
    return json.loads(request.body.decode("utf-8") or "{}")


def _template_to_dict(template):
    return {
        "id": template.id,
        "name": template.name,
        "notification_type": template.notification_type,
        "subject": template.subject,
        "body": template.body,
        "is_active": template.is_active,
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def template_collection(request):
    if request.method == "GET":
        templates = NotificationTemplate.objects.all()
        return JsonResponse({"results": [_template_to_dict(template) for template in templates]})
    template = NotificationTemplate.objects.create(**_json_body(request))
    return JsonResponse(_template_to_dict(template), status=201)


@csrf_exempt
@require_http_methods(["POST"])
def queue_expiration_reminders(request):
    data = _json_body(request)
    queued = queue_membership_expiration_reminders(days_before=int(data.get("days_before", 7)))
    return JsonResponse({"queued": queued})


@csrf_exempt
@require_http_methods(["POST"])
def send_pending_notifications(request):
    return JsonResponse(send_pending_email_notifications())

# Create your views here.
