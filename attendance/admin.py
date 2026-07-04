from django.contrib import admin

from .models import AttendanceCredential, AttendanceRecord


@admin.register(AttendanceCredential)
class AttendanceCredentialAdmin(admin.ModelAdmin):
    list_display = ("member", "token", "is_active", "created_at", "rotated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("member__first_name", "member__last_name", "member__document_number", "token")


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("member", "check_in_at", "check_out_at", "source", "duration_minutes")
    list_filter = ("source", "check_in_at", "check_out_at")
    search_fields = ("member__first_name", "member__last_name", "member__document_number")
