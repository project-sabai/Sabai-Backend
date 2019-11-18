from django import forms
from clinicmodels.models import MedicalVitals


class MedicalVitalsForm(forms.ModelForm):
    class Meta:
        model = MedicalVitals
        fields = [
            'visit', 
            'height', 
            'weight', 
            'systolic', 
            'diastolic',
            'temperature', 
            'hiv_positive', 
            'ptb_positive', 
            'hepc_positive',
            'heart_rate'
        ]