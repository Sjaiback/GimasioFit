from django.urls import path

from . import views

urlpatterns = [
    path("", views.member_collection, name="member_collection"),
    path("<int:member_id>/", views.member_detail, name="member_detail"),
    path("<int:member_id>/history/", views.member_history, name="member_history"),
]
