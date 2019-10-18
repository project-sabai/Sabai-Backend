from django import forms
from clinicmodels.models import Addendum


class AddendumForm(forms.ModelForm):
    class Meta:
        model = Addendum
        fields = [
            'notes',
            'doctor',
            'created_at'
        ]