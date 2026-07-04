from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from accounts.security import ADMIN, MANAGER, RECEPTION, role_required, user_role
from attendance.models import AttendanceRecord
from attendance.services import (
    get_or_create_credential,
    register_attendance_from_payload,
    register_manual_attendance,
)
from billing.models import Debt, Invoice, Payment
from billing.services import issue_invoice_for_payment
from members.models import Member
from memberships.models import Membership, MembershipPlan
from reports.services import administrative_metrics, dashboard_metrics

from .forms import DebtForm, MemberForm, MembershipForm, MembershipPlanForm, PaymentForm


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("frontend:dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect(request.GET.get("next") or "frontend:dashboard")
        messages.error(request, "Credenciales invalidas o usuario inactivo.")

    return render(request, "frontend/login.html")


def logout_view(request):
    logout(request)
    return redirect("frontend:login")


def not_found(request, exception):
    return render(request, "frontend/404.html", status=404)


@role_required(ADMIN, MANAGER, RECEPTION)
def dashboard(request):
    return render(
        request,
        "frontend/dashboard.html",
        {
            "dashboard": dashboard_metrics(),
            "admin_report": administrative_metrics(),
            "recent_members": Member.objects.order_by("-joined_at")[:6],
            "recent_payments": Payment.objects.select_related("member").order_by("-paid_at")[:6],
            "today_attendance": AttendanceRecord.objects.filter(check_in_at__date=timezone.localdate()).count(),
            "current_role": user_role(request.user),
        },
    )


@role_required(ADMIN, MANAGER, RECEPTION)
@require_http_methods(["GET", "POST"])
def members(request):
    form = MemberForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Socio registrado correctamente.")
        return redirect("frontend:members")

    search = request.GET.get("search", "")
    members_query = Member.objects.all()
    if search:
        members_query = members_query.filter(
            Q(document_number__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )
    return render(
        request,
        "frontend/members.html",
        {"form": form, "members": members_query[:80], "search": search},
    )


@role_required(ADMIN, MANAGER)
@require_http_methods(["GET", "POST"])
def memberships(request):
    plan_form = MembershipPlanForm(prefix="plan")
    membership_form = MembershipForm(prefix="membership")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_plan":
            plan_form = MembershipPlanForm(request.POST, prefix="plan")
            if plan_form.is_valid():
                plan_form.save()
                messages.success(request, "Plan creado correctamente.")
                return redirect("frontend:memberships")
        elif action == "create_membership":
            membership_form = MembershipForm(request.POST, prefix="membership")
            if membership_form.is_valid():
                membership_form.save()
                messages.success(request, "Membresia registrada correctamente.")
                return redirect("frontend:memberships")

    return render(
        request,
        "frontend/memberships.html",
        {
            "plan_form": plan_form,
            "membership_form": membership_form,
            "plans": MembershipPlan.objects.all(),
            "memberships": Membership.objects.select_related("member", "plan")[:80],
        },
    )


@role_required(ADMIN, MANAGER, RECEPTION)
@require_http_methods(["GET", "POST"])
def billing(request):
    payment_form = PaymentForm(prefix="payment")
    debt_form = DebtForm(prefix="debt")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_payment":
            payment_form = PaymentForm(request.POST, prefix="payment")
            if payment_form.is_valid():
                payment = payment_form.save()
                messages.success(request, "Pago registrado correctamente.")
                if payment.status == Payment.Status.VERIFIED:
                    issue_invoice_for_payment(payment.id)
                    messages.success(request, "Comprobante emitido automaticamente.")
                return redirect("frontend:billing")
        elif action == "create_debt":
            if not has_management_access(request.user):
                messages.error(request, "No tienes permisos para registrar deudas.")
                return redirect("frontend:billing")
            debt_form = DebtForm(request.POST, prefix="debt")
            if debt_form.is_valid():
                debt_form.save()
                messages.success(request, "Deuda registrada correctamente.")
                return redirect("frontend:billing")
        elif action == "verify_payment":
            if not has_management_access(request.user):
                messages.error(request, "No tienes permisos para verificar pagos.")
                return redirect("frontend:billing")
            payment = Payment.objects.get(pk=request.POST["payment_id"])
            payment.verify()
            issue_invoice_for_payment(payment.id)
            messages.success(request, "Pago verificado y comprobante emitido.")
            return redirect("frontend:billing")

    return render(
        request,
        "frontend/billing.html",
        {
            "payment_form": payment_form,
            "debt_form": debt_form,
            "payments": Payment.objects.select_related("member", "membership", "service")[:80],
            "debts": Debt.objects.select_related("member")[:80],
            "invoices": Invoice.objects.select_related("payment", "payment__member")[:30],
        },
    )


def has_management_access(user):
    return user_role(user) in {ADMIN, MANAGER}


@role_required(ADMIN, MANAGER, RECEPTION)
@require_http_methods(["GET", "POST"])
def attendance(request):
    scan_result = None
    if request.method == "POST":
        action = request.POST.get("action")
        try:
            if action == "scan_payload":
                scan_result = register_attendance_from_payload(request.POST["payload"])
            elif action == "manual_member":
                scan_result = register_manual_attendance(request.POST["member_id"])
            if scan_result:
                movement = "entrada" if scan_result["action"] == "check_in" else "salida"
                messages.success(request, f"{scan_result['member']} registro {movement} correctamente.")
                return redirect("frontend:attendance")
        except Exception as exc:
            messages.error(request, f"No se pudo registrar la asistencia: {exc}")

    today = timezone.localdate()
    members = Member.objects.all()[:80]
    for member in members:
        get_or_create_credential(member)

    return render(
        request,
        "frontend/attendance.html",
        {
            "members": members,
            "records": AttendanceRecord.objects.select_related("member").filter(check_in_at__date=today)[:120],
            "open_records": AttendanceRecord.objects.select_related("member").filter(check_out_at__isnull=True),
        },
    )
