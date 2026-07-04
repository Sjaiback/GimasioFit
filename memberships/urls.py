from django.urls import path

from . import views

urlpatterns = [
    path("plans/", views.plan_collection, name="plan_collection"),
    path("", views.membership_collection, name="membership_collection"),
    path("<int:membership_id>/renew/", views.renew_membership, name="renew_membership"),
    path("<int:membership_id>/suspend/", views.suspend_membership, name="suspend_membership"),
    path("<int:membership_id>/cancel/", views.cancel_membership, name="cancel_membership"),
]
