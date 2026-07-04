from django.db import models
from django.utils import timezone


class Member(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        INACTIVE = "inactive", "Inactivo"
        SUSPENDED = "suspended", "Suspendido"
        CANCELLED = "cancelled", "Cancelado"

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=120, blank=True)
    document_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    emergency_contact = models.CharField(max_length=120, blank=True)
    emergency_phone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    notes = models.TextField(blank=True)
    joined_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["first_name", "last_name"]
        indexes = [
            models.Index(fields=["document_number"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

# Create your models here.
