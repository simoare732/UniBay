from django import forms
from django.db import transaction
from .models import Product

class product_create_form(forms.ModelForm):
    title = forms.CharField(
        label='Titolo',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titolo'}),
    )

    description = forms.CharField(
        label='Descrizione',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    price = forms.DecimalField(
        label='Prezzo',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '99.99'}),
    )

    quantity = forms.IntegerField(
        label='Quantità',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1'}),
    )

    image1 = forms.ImageField(
        label='Immagine 1',
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
    )

    class Meta:
        model = Product
        fields = ['title', 'description', 'image1', 'price', 'quantity']

