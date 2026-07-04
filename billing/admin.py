from django.contrib import admin

from .models import AdditionalService, Debt, Invoice, Payment


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("member", "membership", "amount", "method", "status", "paid_at", "verified_at")
    list_filter = ("method", "status", "paid_at")
    search_fields = ("member__first_name", "member__last_name", "member__document_number")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "payment", "total", "status", "issued_at")
    list_filter = ("status", "issued_at")
    search_fields = ("number",)


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ("member", "concept", "amount", "due_date", "status")
    list_filter = ("status", "due_date")
    search_fields = ("member__first_name", "member__last_name", "concept")

# Register your models here.
