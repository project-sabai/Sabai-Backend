from django import forms
from clinicmodels.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'medicine',
            'quantity',
            'visit',
            'consult',
            'notes',
            'remarks',
            'order_status',
        ]