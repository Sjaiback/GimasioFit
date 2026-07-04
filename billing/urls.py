from django.urls import path

from . import views

urlpatterns = [
    path("payments/", views.payment_collection, name="payment_collection"),
    path("payments/<int:payment_id>/verify/", views.verify_payment, name="verify_payment"),
    path("invoices/", views.invoice_collection, name="invoice_collection"),
    path("debts/", views.debt_collection, name="debt_collection"),
]
