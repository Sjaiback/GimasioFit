from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "document_number", "phone", "email", "status", "joined_at")
    list_filter = ("status", "joined_at")
    search_fields = ("first_name", "last_name", "document_number", "email", "phone")

# Register your models here.
