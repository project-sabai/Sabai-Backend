from django import forms
from clinicmodels.models import DentalVitals


class DentalVitalsForm(forms.ModelForm):
    class Meta:
        model = DentalVitals
        fields = [
            'visit',
            'complaints',
            'intraoral',
            'diagnosis',
            'exo',
            'cap',
            'f',
            'others',
        ]