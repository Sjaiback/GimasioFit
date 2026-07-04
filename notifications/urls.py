from django.urls import path

from . import views

urlpatterns = [
    path("templates/", views.template_collection, name="template_collection"),
    path("expiration-reminders/", views.queue_expiration_reminders, name="queue_expiration_reminders"),
    path("send-pending/", views.send_pending_notifications, name="send_pending_notifications"),
]
