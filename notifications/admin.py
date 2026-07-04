from django.contrib import admin

from .models import NotificationLog, NotificationTemplate


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "notification_type", "subject", "is_active")
    list_filter = ("notification_type", "is_active")
    search_fields = ("name", "subject")


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("member", "email", "subject", "status", "scheduled_for", "sent_at")
    list_filter = ("status", "scheduled_for")
    search_fields = ("email", "subject", "member__first_name", "member__last_name")

# Register your models here.
