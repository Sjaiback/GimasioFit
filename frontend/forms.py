from django import forms

from billing.models import Debt, Payment
from members.models import Member
from memberships.models import Membership, MembershipPlan


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            "first_name",
            "last_name",
            "document_number",
            "birth_date",
            "phone",
            "email",
            "address",
            "emergency_contact",
            "emergency_phone",
            "status",
            "notes",
        ]
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "document_number": "DNI",
            "birth_date": "Fecha de nacimiento",
            "phone": "Telefono",
            "email": "Correo",
            "address": "Direccion",
            "emergency_contact": "Contacto de emergencia",
            "emergency_phone": "Telefono de emergencia",
            "status": "Estado",
            "notes": "Notas",
        }
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class MembershipPlanForm(forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ["name", "duration_months", "price", "description", "is_active"]
        labels = {
            "name": "Nombre",
            "duration_months": "Duracion",
            "price": "Precio",
            "description": "Descripcion",
            "is_active": "Activo",
        }
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ["member", "plan", "start_date", "end_date", "status"]
        labels = {
            "member": "Socio",
            "plan": "Plan",
            "start_date": "Fecha de inicio",
            "end_date": "Fecha de fin",
            "status": "Estado",
        }
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["member", "membership", "service", "amount", "method", "status", "notes"]
        labels = {
            "member": "Socio",
            "membership": "Membresia",
            "service": "Servicio adicional",
            "amount": "Monto",
            "method": "Metodo",
            "status": "Estado",
            "notes": "Notas",
        }
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}


class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ["member", "concept", "amount", "due_date", "status"]
        labels = {
            "member": "Socio",
            "concept": "Concepto",
            "amount": "Monto",
            "due_date": "Fecha de vencimiento",
            "status": "Estado",
        }
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}
