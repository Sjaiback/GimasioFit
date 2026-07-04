import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from members.models import Member

from .models import AttendanceCredential, AttendanceRecord
from .serializers import attendance_record_to_dict
from .services import (
    get_or_create_credential,
    qr_png_for_member,
    register_attendance_from_payload,
)


def _json_body(request):
    return json.loads(request.body.decode("utf-8") or "{}")


@require_http_methods(["GET"])
def attendance_collection(request):
    records = AttendanceRecord.objects.select_related("member")
    return JsonResponse({"results": [attendance_record_to_dict(record) for record in records[:100]]})


@csrf_exempt
@require_http_methods(["POST"])
def scan_attendance(request):
    data = _json_body(request)
    result = register_attendance_from_payload(data["payload"])
    return JsonResponse(
        {
            "action": result["action"],
            "member": str(result["member"]),
            "has_active_membership": result["has_active_membership"],
            "record": attendance_record_to_dict(result["record"]),
        }
    )


@require_http_methods(["GET"])
def member_qr(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    return HttpResponse(qr_png_for_member(member), content_type="image/png")


@csrf_exempt
@require_http_methods(["POST"])
def rotate_member_qr(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    credential = get_or_create_credential(member)
    credential.rotate()
    return JsonResponse({"token": str(credential.token)})


@require_http_methods(["GET"])
def credential_collection(request):
    credentials = AttendanceCredential.objects.select_related("member")
    return JsonResponse(
        {
            "results": [
                {
                    "member_id": credential.member_id,
                    "member": str(credential.member),
                    "token": str(credential.token),
                    "is_active": credential.is_active,
                }
                for credential in credentials
            ]
        }
    )
