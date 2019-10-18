from django import forms
from clinicmodels.models import Medication


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = [
            'medicine_name',
            'reserve_quantity',
            'quantity',
            'notes',
            'remarks'
        ]