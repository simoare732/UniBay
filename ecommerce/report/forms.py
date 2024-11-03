from django import forms
from .models import Report, Strike

class report_create_form(forms.ModelForm):
    reason = forms.ChoiceField(
        choices=Report.reason_choices,
        label='Motivo',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        label='Descrizione',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Inserisci una descrizione del problema'}),
    )

    class Meta:
        model = Report
        fields = ['reason', 'description']


class strike_create_form(forms.ModelForm):
    description = forms.CharField(
        label='Motivo',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Strike dovuto a...'}),
    )

    class Meta:
        model = Strike
        fields = ['description']