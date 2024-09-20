from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field


class UserRegisterForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('CLIENTE', 'Cliente'),
        ('VENDITORE', 'Venditore'),
    )

    # Common fields
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-select', 'id': 'user-type'}),
                                  label="Tipo di Utente")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    # Fields for 'CLIENTE'
    nome = forms.CharField(max_length=50, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'nome-field'}))
    cognome = forms.CharField(max_length=50, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'cognome-field'}))

    # Fields for 'VENDITORE'
    partita_iva = forms.CharField(max_length=20, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'partita-iva-field'}))
    email_aziendale = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'id': 'email-aziendale-field'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'email',
            'password1',
            'password2',
            'user_type',
            Div(
                Field('nome'),
                Field('cognome'),
                css_class="cliente-fields"
            ),
            Div(
                Field('partita_iva'),
                Field('email_aziendale'),
                css_class="venditore-fields"
            ),
            Submit('submit', 'Registrati', css_class="btn btn-primary")
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = user.profile
            profile.user_type = self.cleaned_data['user_type']
            profile.nome = self.cleaned_data.get('nome', '')
            profile.cognome = self.cleaned_data.get('cognome', '')
            profile.partita_iva = self.cleaned_data.get('partita_iva', '')
            profile.email_aziendale = self.cleaned_data.get('email_aziendale', '')
            profile.save()
        return user
