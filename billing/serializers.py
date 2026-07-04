def payment_to_dict(payment):
    return {
        "id": payment.id,
        "member_id": payment.member_id,
        "member": str(payment.member),
        "membership_id": payment.membership_id,
        "service_id": payment.service_id,
        "amount": str(payment.amount),
        "method": payment.method,
        "status": payment.status,
        "receipt_file": payment.receipt_file.url if payment.receipt_file else None,
        "paid_at": payment.paid_at.isoformat(),
        "verified_at": payment.verified_at.isoformat() if payment.verified_at else None,
        "notes": payment.notes,
    }


def debt_to_dict(debt):
    return {
        "id": debt.id,
        "member_id": debt.member_id,
        "member": str(debt.member),
        "concept": debt.concept,
        "amount": str(debt.amount),
        "due_date": debt.due_date.isoformat(),
        "status": debt.status,
    }


def invoice_to_dict(invoice):
    return {
        "id": invoice.id,
        "payment_id": invoice.payment_id,
        "number": invoice.number,
        "issued_at": invoice.issued_at.isoformat(),
        "subtotal": str(invoice.subtotal),
        "tax": str(invoice.tax),
        "total": str(invoice.total),
        "status": invoice.status,
    }
