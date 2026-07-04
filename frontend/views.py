from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from billing.models import Debt, Invoice, Payment
from billing.services import issue_invoice_for_payment
from members.models import Member
from memberships.models import Membership, MembershipPlan
from reports.services import administrative_metrics, dashboard_metrics

from .forms import DebtForm, MemberForm, MembershipForm, MembershipPlanForm, PaymentForm


def dashboard(request):
    return render(
        request,
        "frontend/dashboard.html",
        {
            "dashboard": dashboard_metrics(),
            "admin_report": administrative_metrics(),
            "recent_members": Member.objects.order_by("-joined_at")[:6],
            "recent_payments": Payment.objects.select_related("member").order_by("-paid_at")[:6],
        },
    )


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
            debt_form = DebtForm(request.POST, prefix="debt")
            if debt_form.is_valid():
                debt_form.save()
                messages.success(request, "Deuda registrada correctamente.")
                return redirect("frontend:billing")
        elif action == "verify_payment":
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
