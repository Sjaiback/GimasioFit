from django.contrib import admin

from .models import Membership, MembershipPlan


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_months", "price", "is_active")
    list_filter = ("duration_months", "is_active")
    search_fields = ("name",)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("member", "plan", "start_date", "end_date", "status", "renewal_count")
    list_filter = ("status", "plan")
    search_fields = ("member__first_name", "member__last_name", "member__document_number")

# Register your models here.
