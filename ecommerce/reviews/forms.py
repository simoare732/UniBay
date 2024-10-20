from django import forms
from .models import Review, Seller_Review


class review_create_form(forms.ModelForm):
    title = forms.CharField(
        max_length=100, required=True,
        label='Titolo',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quali sono le cose più importanti da sapere?'}),
    )

    comment = forms.CharField(
        label='Aggiungi una recensione scritta',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Che cosa ti è piaciuto e che cosa no?'}),
    )

    rating = forms.IntegerField(
        required=True,
        label='Valutazione complessiva',
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'rating'}),
    )

    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']

class seller_review_create_form(forms.ModelForm):
    title = forms.CharField(
        max_length=100, required=True,
        label='Titolo',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quali sono le cose più importanti da sapere?'}),
    )

    comment = forms.CharField(
        label='Aggiungi una recensione scritta',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Che cosa ti è piaciuto e che cosa no?'}),
    )

    class Meta:
        model = Seller_Review
        fields = ['title', 'comment']