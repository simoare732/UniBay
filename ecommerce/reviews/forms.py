from django import forms
from .models import Review

class review_create_form(forms.ModelForm):
    title = forms.CharField(
        label='Titolo',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quali sono le cose più importanti da sapere?'}),
    )

    description = forms.CharField(
        label='Aggiungi una recensione scritta',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Che cosa ti è piaciuto e che cosa no?'}),
    )

    rating = forms.IntegerField(
        label='Valutazione complessiva',
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'rating'}),
    )

    class Meta:
        model = Review
        fields = ['rating', 'title', 'description']
