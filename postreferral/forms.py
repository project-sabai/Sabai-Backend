from django import forms
from clinicmodels.models import Postreferral


class PostreferralForm(forms.ModelForm):
    class Meta:
        model = Postreferral
        fields = ['visit', 'recorder', 'remarks']
