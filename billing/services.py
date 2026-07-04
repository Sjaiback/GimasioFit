from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from .models import Invoice, Payment


@transaction.atomic
def issue_invoice_for_payment(payment_id, tax_rate=Decimal("0.00")):
    payment = Payment.objects.select_for_update().get(pk=payment_id)
    existing = getattr(payment, "invoice", None)
    if existing:
        return existing

    subtotal = payment.amount
    tax = (subtotal * Decimal(str(tax_rate))).quantize(Decimal("0.01"))
    total = subtotal + tax
    number = f"CF-{timezone.now():%Y%m%d}-{payment.id:06d}"
    return Invoice.objects.create(
        payment=payment,
        number=number,
        subtotal=subtotal,
        tax=tax,
        total=total,
    )
