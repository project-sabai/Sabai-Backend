from django import forms
from clinicmodels.models import Consult


class ConsultForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ['visit', 'type', 'doctor', 'notes', 'diagnosis', 'problems',
                  'urine_test', 'hemocue_count', 'blood_glucose',
                  'referrals', 'chronic_referral', 'treatments_done']