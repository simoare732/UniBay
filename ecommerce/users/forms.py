from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Registered_User, Seller


class User_Signup_Form(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'username@example.com'}),
        error_messages={'required': 'Questo campo è obbligatorio.'},
    )
    phone = forms.CharField(
        max_length=20,
        label='Cellulare',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
        error_messages = {'required': 'Questo campo è obbligatorio.'},
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Nome utente',
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password',
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Conferma Password',
    )

    class Meta:
        model = User
        fields = ['email', 'username',  'password1', 'password2', 'phone']

    # This decoration ensure that the save method is atomic, meaning that if an error occurs during the save process,
    # all the transaction is rolled back.
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_registered_user = True
        user.save()
        registered_user = Registered_User.objects.create(user=user)
        registered_user.email = self.cleaned_data.get('email')
        registered_user.phone = self.cleaned_data.get('phone')
        registered_user.save()
        return user


class Seller_Signup_Form(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'username@example.com'}),
        error_messages={'required': 'Questo campo è obbligatorio.'},
    )
    phone = forms.CharField(
        max_length=20,
        label='Cellulare',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
        error_messages={'required': 'Questo campo è obbligatorio.'},
    )

    PIVA = forms.CharField(
        max_length=15,
        label='Partita IVA',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678901'}),
        error_messages={'required': 'Questo campo è obbligatorio.'},
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Nome utente',
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password',
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Conferma Password',
    )

    class Meta:
        model = User
        fields = ['email', 'PIVA', 'username',  'password1', 'password2', 'phone']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        user.save()
        seller = Seller.objects.create(user=user)
        seller.email = self.cleaned_data.get('email')
        seller.phone = self.cleaned_data.get('phone')
        seller.PIVA = self.cleaned_data.get('PIVA')
        seller.save()
        return user