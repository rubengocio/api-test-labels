from django import forms

from manager_testing import Constants
from manager_testing.models import Carrier


class CarrierForm(forms.ModelForm):
    site = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Constants.CHOICES_SITES)
    code = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    enabled = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Carrier
        fields = (
            'site',
            'code',
            'name',
            'enabled',
        )
