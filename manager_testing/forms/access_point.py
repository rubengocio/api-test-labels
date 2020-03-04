from django import forms

from manager_testing import Constants
from manager_testing.models import Carrier, AccessPoint


class AccessPointForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    url = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = AccessPoint
        fields = (
            'name',
            'url',
        )
