import json

from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from accounts.security import ADMIN, MANAGER, RECEPTION, role_required

from .models import Member
from .serializers import member_to_dict


def _json_body(request):
    return json.loads(request.body.decode("utf-8") or "{}")


@csrf_exempt
@role_required(ADMIN, MANAGER, RECEPTION)
@require_http_methods(["GET", "POST"])
def member_collection(request):
    if request.method == "GET":
        members = Member.objects.all()
        status = request.GET.get("status")
        search = request.GET.get("search")
        if status:
            members = members.filter(status=status)
        if search:
            members = members.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(document_number__icontains=search)
            )
        return JsonResponse({"results": [member_to_dict(member) for member in members]})

    data = _json_body(request)
    member = Member.objects.create(**data)
    return JsonResponse(member_to_dict(member), status=201)


@csrf_exempt
@role_required(ADMIN, MANAGER, RECEPTION)
@require_http_methods(["GET", "PATCH", "DELETE"])
def member_detail(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    if request.method == "GET":
        return JsonResponse(member_to_dict(member))
    if request.method == "DELETE":
        member.status = Member.Status.INACTIVE
        member.save(update_fields=["status", "updated_at"])
        return JsonResponse({"status": "inactive"})

    data = _json_body(request)
    for field, value in data.items():
        if field in model_to_dict(member):
            setattr(member, field, value)
    member.save()
    return JsonResponse(member_to_dict(member))


@role_required(ADMIN, MANAGER, RECEPTION)
@require_http_methods(["GET"])
def member_history(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    memberships = [
        {
            "id": item.id,
            "plan": item.plan.name,
            "start_date": item.start_date.isoformat(),
            "end_date": item.end_date.isoformat(),
            "status": item.status,
        }
        for item in member.memberships.select_related("plan")
    ]
    payments = [
        {
            "id": payment.id,
            "amount": str(payment.amount),
            "method": payment.method,
            "status": payment.status,
            "paid_at": payment.paid_at.isoformat(),
        }
        for payment in member.payments.all()
    ]
    return JsonResponse({"member": member_to_dict(member), "memberships": memberships, "payments": payments})

# Create your views here.
