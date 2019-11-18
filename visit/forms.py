from django import forms
from clinicmodels.models import Visit


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        # fields = ['patient', 'status', 'medical_consultation', 'dental_consultation']
        # fields = ['id', 'patient', 'status', 'consultations','created_at']
        fields = ['id', 'patient', 'status', 'consultations', 'visit_date']

