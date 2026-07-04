from django.urls import path

from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("socios/", views.members, name="members"),
    path("membresias/", views.memberships, name="memberships"),
    path("pagos/", views.billing, name="billing"),
]
