import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from accounts.security import ADMIN, MANAGER, RECEPTION, role_required

from .models import Debt, Invoice, Payment
from .serializers import debt_to_dict, invoice_to_dict, payment_to_dict
from .services import issue_invoice_for_payment


def _json_body(request):
    return json.loads(request.body.decode("utf-8") or "{}")


@csrf_exempt
@role_required(ADMIN, MANAGER, RECEPTION)
@require_http_methods(["GET", "POST"])
def payment_collection(request):
    if request.method == "GET":
        payments = Payment.objects.select_related("member", "membership", "service")
        status = request.GET.get("status")
        if status:
            payments = payments.filter(status=status)
        return JsonResponse({"results": [payment_to_dict(payment) for payment in payments]})

    data = _json_body(request)
    payment = Payment.objects.create(
        member_id=data["member_id"],
        membership_id=data.get("membership_id"),
        service_id=data.get("service_id"),
        amount=data["amount"],
        method=data["method"],
        status=data.get("status", Payment.Status.PENDING),
        notes=data.get("notes", ""),
    )
    return JsonResponse(payment_to_dict(payment), status=201)


@csrf_exempt
@role_required(ADMIN, MANAGER)
@require_http_methods(["POST"])
def verify_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    payment.verify()
    return JsonResponse(payment_to_dict(payment))


@csrf_exempt
@role_required(ADMIN, MANAGER)
@require_http_methods(["GET", "POST"])
def invoice_collection(request):
    if request.method == "GET":
        invoices = Invoice.objects.select_related("payment", "payment__member")
        return JsonResponse({"results": [invoice_to_dict(invoice) for invoice in invoices]})

    data = _json_body(request)
    invoice = issue_invoice_for_payment(data["payment_id"], data.get("tax_rate", "0.00"))
    return JsonResponse(invoice_to_dict(invoice), status=201)


@csrf_exempt
@role_required(ADMIN, MANAGER)
@require_http_methods(["GET", "POST"])
def debt_collection(request):
    if request.method == "GET":
        debts = Debt.objects.select_related("member")
        status = request.GET.get("status")
        if status:
            debts = debts.filter(status=status)
        return JsonResponse({"results": [debt_to_dict(debt) for debt in debts]})

    debt = Debt.objects.create(**_json_body(request))
    return JsonResponse(debt_to_dict(debt), status=201)

# Create your views here.
