from django.urls import path

from . import views

urlpatterns = [
    path("administrative/", views.administrative_report, name="administrative_report"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
