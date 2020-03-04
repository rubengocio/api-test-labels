from django import forms

from manager_testing.models import Service, Carrier, AccessPoint, Test


class TestForm(forms.ModelForm):
    access_point_a = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                            queryset=AccessPoint.objects.all())
    access_point_b = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                            queryset=AccessPoint.objects.all())

    release = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Test
        fields = (
            'access_point_a',
            'access_point_b',
            'release',
        )


