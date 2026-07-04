from datetime import timedelta

from django.db import models
from django.utils import timezone


class MembershipPlan(models.Model):
    class Duration(models.IntegerChoices):
        MONTHLY = 1, "Mensual"
        QUARTERLY = 3, "Trimestral"
        SEMIANNUAL = 6, "Semestral"
        ANNUAL = 12, "Anual"

    name = models.CharField(max_length=80, unique=True)
    duration_months = models.PositiveSmallIntegerField(choices=Duration.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["duration_months", "price"]

    def __str__(self):
        return self.name


class Membership(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Activa"
        PENDING = "pending", "Pendiente"
        SUSPENDED = "suspended", "Suspendida"
        CANCELLED = "cancelled", "Cancelada"
        EXPIRED = "expired", "Vencida"

    member = models.ForeignKey("members.Member", on_delete=models.CASCADE, related_name="memberships")
    plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT, related_name="memberships")
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    renewal_count = models.PositiveIntegerField(default=0)
    suspended_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-end_date"]
        indexes = [
            models.Index(fields=["status", "end_date"]),
            models.Index(fields=["member", "status"]),
        ]

    def __str__(self):
        return f"{self.member} - {self.plan}"

    @property
    def days_to_expire(self):
        return (self.end_date - timezone.localdate()).days

    def renew(self):
        base_date = max(self.end_date, timezone.localdate())
        self.start_date = timezone.localdate()
        self.end_date = base_date + timedelta(days=30 * self.plan.duration_months)
        self.status = self.Status.ACTIVE
        self.renewal_count += 1
        self.save(update_fields=["start_date", "end_date", "status", "renewal_count", "updated_at"])

    def suspend(self):
        self.status = self.Status.SUSPENDED
        self.suspended_at = timezone.now()
        self.save(update_fields=["status", "suspended_at", "updated_at"])

    def cancel(self):
        self.status = self.Status.CANCELLED
        self.cancelled_at = timezone.now()
        self.save(update_fields=["status", "cancelled_at", "updated_at"])

# Create your models here.
