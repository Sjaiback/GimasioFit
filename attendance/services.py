from io import BytesIO

from django.db import transaction
from django.utils import timezone

from members.models import Member
from memberships.models import Membership

from .models import AttendanceCredential, AttendanceRecord


def get_or_create_credential(member):
    credential, _ = AttendanceCredential.objects.get_or_create(member=member)
    return credential


def qr_payload_for_member(member):
    credential = get_or_create_credential(member)
    return f"CONTROLFIT-ATTENDANCE:{credential.token}"


def qr_png_for_member(member):
    import qrcode

    image = qrcode.make(qr_payload_for_member(member))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def normalize_token(payload):
    raw = payload.strip()
    if ":" in raw:
        raw = raw.rsplit(":", 1)[-1]
    return raw


def member_has_active_membership(member):
    today = timezone.localdate()
    return Membership.objects.filter(
        member=member,
        status=Membership.Status.ACTIVE,
        start_date__lte=today,
        end_date__gte=today,
    ).exists()


@transaction.atomic
def register_attendance_from_payload(payload, source=AttendanceRecord.Source.QR):
    token = normalize_token(payload)
    credential = AttendanceCredential.objects.select_for_update().select_related("member").get(
        token=token,
        is_active=True,
    )
    member = credential.member
    open_record = AttendanceRecord.objects.select_for_update().filter(
        member=member,
        check_out_at__isnull=True,
    ).order_by("-check_in_at").first()

    if open_record:
        open_record.check_out_at = timezone.now()
        open_record.save(update_fields=["check_out_at"])
        action = "check_out"
        record = open_record
    else:
        record = AttendanceRecord.objects.create(member=member, source=source)
        action = "check_in"

    return {
        "action": action,
        "record": record,
        "member": member,
        "has_active_membership": member_has_active_membership(member),
    }


def register_manual_attendance(member_id):
    member = Member.objects.get(pk=member_id)
    credential = get_or_create_credential(member)
    return register_attendance_from_payload(str(credential.token), source=AttendanceRecord.Source.MANUAL)
