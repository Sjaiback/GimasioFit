from datetime import timedelta

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from billing.models import Debt, Payment
from members.models import Member
from memberships.models import Membership


def administrative_metrics():
    income_by_month = (
        Payment.objects.filter(status=Payment.Status.VERIFIED)
        .annotate(month=TruncMonth("paid_at"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )
    return {
        "verified_income": str(
            Payment.objects.filter(status=Payment.Status.VERIFIED).aggregate(total=Sum("amount"))["total"] or 0
        ),
        "pending_debt": str(Debt.objects.filter(status=Debt.Status.PENDING).aggregate(total=Sum("amount"))["total"] or 0),
        "active_memberships": Membership.objects.filter(status=Membership.Status.ACTIVE).count(),
        "members_by_status": list(Member.objects.values("status").annotate(total=Count("id")).order_by("status")),
        "income_by_month": [
            {"month": item["month"].date().isoformat(), "total": str(item["total"] or 0)} for item in income_by_month
        ],
    }


def dashboard_metrics():
    today = timezone.localdate()
    soon = today + timedelta(days=7)
    expiring = Membership.objects.filter(status=Membership.Status.ACTIVE, end_date__range=(today, soon))
    return {
        "total_members": Member.objects.count(),
        "active_members": Member.objects.filter(status=Member.Status.ACTIVE).count(),
        "monthly_income": str(
            Payment.objects.filter(
                status=Payment.Status.VERIFIED,
                paid_at__year=today.year,
                paid_at__month=today.month,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        ),
        "expiring_memberships": expiring.count(),
        "expiration_alerts": [
            {
                "membership_id": item.id,
                "member": str(item.member),
                "end_date": item.end_date.isoformat(),
                "days_to_expire": item.days_to_expire,
            }
            for item in expiring.select_related("member", "plan").order_by("end_date")[:10]
        ],
    }
