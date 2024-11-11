from django import forms


class address_form(forms.Form):
    shipping_address = forms.CharField(label="Indirizzo di spedizione", max_length=255)
    card_number = forms.CharField(label="Numero della carta di credito", max_length=16, min_length=13)
    expiration_date = forms.CharField(label="Data di scadenza (MM/AA)", max_length=5)
    cvv = forms.CharField(label="CVV", max_length=4)