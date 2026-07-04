import json
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Membership, MembershipPlan
from .serializers import membership_to_dict, plan_to_dict


def _json_body(request):
    return json.loads(request.body.decode("utf-8") or "{}")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def plan_collection(request):
    if request.method == "GET":
        plans = MembershipPlan.objects.filter(is_active=True)
        return JsonResponse({"results": [plan_to_dict(plan) for plan in plans]})
    plan = MembershipPlan.objects.create(**_json_body(request))
    return JsonResponse(plan_to_dict(plan), status=201)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def membership_collection(request):
    if request.method == "GET":
        memberships = Membership.objects.select_related("member", "plan")
        status = request.GET.get("status")
        if status:
            memberships = memberships.filter(status=status)
        return JsonResponse({"results": [membership_to_dict(item) for item in memberships]})

    data = _json_body(request)
    plan = get_object_or_404(MembershipPlan, pk=data["plan_id"])
    start_date = timezone.localdate()
    membership = Membership.objects.create(
        member_id=data["member_id"],
        plan=plan,
        start_date=data.get("start_date", start_date),
        end_date=data.get("end_date", start_date + timedelta(days=30 * plan.duration_months)),
        status=data.get("status", Membership.Status.ACTIVE),
    )
    return JsonResponse(membership_to_dict(membership), status=201)


@csrf_exempt
@require_http_methods(["POST"])
def renew_membership(request, membership_id):
    membership = get_object_or_404(Membership, pk=membership_id)
    membership.renew()
    return JsonResponse(membership_to_dict(membership))


@csrf_exempt
@require_http_methods(["POST"])
def suspend_membership(request, membership_id):
    membership = get_object_or_404(Membership, pk=membership_id)
    membership.suspend()
    return JsonResponse(membership_to_dict(membership))


@csrf_exempt
@require_http_methods(["POST"])
def cancel_membership(request, membership_id):
    membership = get_object_or_404(Membership, pk=membership_id)
    membership.cancel()
    return JsonResponse(membership_to_dict(membership))

# Create your views here.
