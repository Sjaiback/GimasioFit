import uuid

from django.db import models
from django.utils import timezone


class AttendanceCredential(models.Model):
    member = models.OneToOneField("members.Member", on_delete=models.CASCADE, related_name="qr_credential")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rotated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["member__first_name", "member__last_name"]

    def __str__(self):
        return f"QR {self.member}"

    def rotate(self):
        self.token = uuid.uuid4()
        self.rotated_at = timezone.now()
        self.save(update_fields=["token", "rotated_at"])


class AttendanceRecord(models.Model):
    class Source(models.TextChoices):
        QR = "qr", "QR"
        MANUAL = "manual", "Manual"

    member = models.ForeignKey("members.Member", on_delete=models.CASCADE, related_name="attendance_records")
    check_in_at = models.DateTimeField(default=timezone.now)
    check_out_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.QR)
    notes = models.CharField(max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-check_in_at"]
        indexes = [
            models.Index(fields=["member", "check_in_at"]),
            models.Index(fields=["check_out_at"]),
        ]

    def __str__(self):
        return f"{self.member} - {self.check_in_at:%d/%m/%Y %H:%M}"

    @property
    def is_open(self):
        return self.check_out_at is None

    @property
    def duration_minutes(self):
        end = self.check_out_at or timezone.now()
        return int((end - self.check_in_at).total_seconds() // 60)
