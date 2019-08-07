from django import forms
from clinicmodels.models import Patient

class NewPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['village_prefix', 'name', 'image',
                  'contact_no', 'gender', 'travelling_time_to_village',
                  'date_of_birth', 'drug_allergy', 'parent', 'face_encodings']