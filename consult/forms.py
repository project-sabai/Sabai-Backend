from django import forms
from clinicmodels.models import Consult


class ConsultForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = [ 
            'id',
            'visit', 
            'type', 
            'doctor', 
            'notes', 
            'diagnosis', 
            'problems',
            'exo',
            'cap',
            'sdf',
            'f',
            'others',
            'referred_for',
            'sub_type',
            'created_at'
            ]