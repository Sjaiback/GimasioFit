from django.db import models
from django.utils import timezone


class AdditionalService(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = "cash", "Efectivo"
        CARD = "card", "Tarjeta"
        TRANSFER = "transfer", "Transferencia"
        DIGITAL_WALLET = "digital_wallet", "Billetera digital"

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        VERIFIED = "verified", "Verificado"
        REJECTED = "rejected", "Rechazado"

    member = models.ForeignKey("members.Member", on_delete=models.PROTECT, related_name="payments")
    membership = models.ForeignKey(
        "memberships.Membership",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    service = models.ForeignKey(AdditionalService, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=30, choices=Method.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    receipt_file = models.FileField(upload_to="receipts/", blank=True)
    paid_at = models.DateTimeField(default=timezone.now)
    verified_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-paid_at"]
        indexes = [
            models.Index(fields=["status", "paid_at"]),
            models.Index(fields=["member", "paid_at"]),
        ]

    def __str__(self):
        return f"{self.member} - {self.amount}"

    def verify(self):
        self.status = self.Status.VERIFIED
        self.verified_at = timezone.now()
        self.save(update_fields=["status", "verified_at"])


class Invoice(models.Model):
    class Status(models.TextChoices):
        ISSUED = "issued", "Emitida"
        PAID = "paid", "Pagada"
        VOID = "void", "Anulada"

    payment = models.OneToOneField(Payment, on_delete=models.PROTECT, related_name="invoice")
    number = models.CharField(max_length=30, unique=True)
    issued_at = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ISSUED)

    class Meta:
        ordering = ["-issued_at"]

    def __str__(self):
        return self.number


class Debt(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        PAID = "paid", "Pagada"
        CANCELLED = "cancelled", "Cancelada"

    member = models.ForeignKey("members.Member", on_delete=models.CASCADE, related_name="debts")
    concept = models.CharField(max_length=160)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["due_date"]
        indexes = [models.Index(fields=["status", "due_date"])]

    def __str__(self):
        return f"{self.member} - {self.concept}"

# Create your models here.
