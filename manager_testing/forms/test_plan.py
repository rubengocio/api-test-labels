from django import forms

from manager_testing import Constants
from manager_testing.models import TestPlan, Service


class TestPlanForm(forms.ModelForm):
    service = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Service.objects.all())
    logistic_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Constants.CHOICES_LOGISTIC_TYPES)
    response_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Constants.CHOICES_RESPONSE_TYPE)
    shipment_id = forms.IntegerField()

    class Meta:
        model = TestPlan
        fields = (
            'service',
            'logistic_type',
            'response_type',
            'shipment_id',
        )
