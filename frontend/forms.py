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
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class MembershipPlanForm(forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ["name", "duration_months", "price", "description", "is_active"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ["member", "plan", "start_date", "end_date", "status"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["member", "membership", "service", "amount", "method", "status", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}


class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ["member", "concept", "amount", "due_date", "status"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}
