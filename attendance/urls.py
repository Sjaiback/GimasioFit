from django.urls import path

from . import views

urlpatterns = [
    path("", views.attendance_collection, name="attendance_collection"),
    path("scan/", views.scan_attendance, name="scan_attendance"),
    path("credentials/", views.credential_collection, name="credential_collection"),
    path("members/<int:member_id>/qr.png", views.member_qr, name="member_qr"),
    path("members/<int:member_id>/rotate/", views.rotate_member_qr, name="rotate_member_qr"),
]
