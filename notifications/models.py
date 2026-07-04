from django.db import models
from django.utils import timezone


class NotificationTemplate(models.Model):
    class Type(models.TextChoices):
        MEMBERSHIP_EXPIRATION = "membership_expiration", "Vencimiento de membresia"
        RESERVATION_CONFIRMED = "reservation_confirmed", "Reserva confirmada"
        PROMOTION = "promotion", "Promocion especial"

    name = models.CharField(max_length=100)
    notification_type = models.CharField(max_length=40, choices=Type.choices)
    subject = models.CharField(max_length=160)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["notification_type", "name"]

    def __str__(self):
        return self.name


class NotificationLog(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "En cola"
        SENT = "sent", "Enviada"
        FAILED = "failed", "Fallida"

    member = models.ForeignKey("members.Member", on_delete=models.CASCADE, related_name="notifications")
    template = models.ForeignKey(NotificationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    scheduled_for = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ["-scheduled_for"]
        indexes = [models.Index(fields=["status", "scheduled_for"])]

    def __str__(self):
        return f"{self.email} - {self.subject}"

# Create your models here.
