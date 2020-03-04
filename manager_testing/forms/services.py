from django import forms

from manager_testing.models import Service, Carrier


class ServiceForm(forms.ModelForm):
    carrier = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Carrier.objects.filter(enabled=True))
    code = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    enabled = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Service
        fields = (
            'carrier',
            'code',
            'name',
            'enabled',
        )
