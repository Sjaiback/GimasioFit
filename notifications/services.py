from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from memberships.models import Membership

from .models import NotificationLog, NotificationTemplate


def queue_membership_expiration_reminders(days_before=7):
    today = timezone.localdate()
    limit = today + timedelta(days=days_before)
    template = NotificationTemplate.objects.filter(
        notification_type=NotificationTemplate.Type.MEMBERSHIP_EXPIRATION,
        is_active=True,
    ).first()

    queued = 0
    memberships = Membership.objects.filter(
        status=Membership.Status.ACTIVE,
        end_date__range=(today, limit),
        member__email__gt="",
    ).select_related("member", "plan")

    for membership in memberships:
        subject = template.subject if template else "Tu membresia esta por vencer"
        body = (
            template.body.format(member=membership.member, end_date=membership.end_date, plan=membership.plan.name)
            if template
            else f"Hola {membership.member}, tu membresia {membership.plan.name} vence el {membership.end_date}."
        )
        exists = NotificationLog.objects.filter(
            member=membership.member,
            subject=subject,
            scheduled_for__date=today,
        ).exists()
        if not exists:
            NotificationLog.objects.create(
                member=membership.member,
                template=template,
                email=membership.member.email,
                subject=subject,
                body=body,
            )
            queued += 1
    return queued


def send_pending_email_notifications(limit=50):
    pending = NotificationLog.objects.filter(
        status=NotificationLog.Status.QUEUED,
        scheduled_for__lte=timezone.now(),
    ).order_by("scheduled_for")[:limit]
    sent = 0
    failed = 0

    for notification in pending:
        try:
            send_mail(
                notification.subject,
                notification.body,
                settings.DEFAULT_FROM_EMAIL,
                [notification.email],
                fail_silently=False,
            )
            notification.status = NotificationLog.Status.SENT
            notification.sent_at = timezone.now()
            notification.error_message = ""
            sent += 1
        except Exception as exc:
            notification.status = NotificationLog.Status.FAILED
            notification.error_message = str(exc)
            failed += 1
        notification.save(update_fields=["status", "sent_at", "error_message"])

    return {"sent": sent, "failed": failed}
