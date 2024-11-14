from django import forms
from .models import Shipping, Payment


class shipping_form(forms.ModelForm):
    country = forms.CharField(
        label="Paese", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        label="Nome", max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    surname = forms.CharField(
        label="Cognome", max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_address = forms.CharField(
        label="Indirizzo di spedizione", max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city = forms.CharField(
        label="Città", max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    zip_code = forms.CharField(
        label="CAP", max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Shipping
        fields = ['country', 'name', 'surname', 'shipping_address', 'city', 'zip_code']


class payment_form(forms.ModelForm):
    card_number = forms.CharField(
        label="Numero della carta di credito", max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    expiration_date = forms.CharField(
        label="Data di scadenza (MM/AA)", max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cvv = forms.CharField(
        label="CVV", max_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Payment
        fields = ['card_number', 'expiration_date', 'cvv']