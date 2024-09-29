from django import forms
from .models import Product, Category

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

    image2 = forms.ImageField(
        label='Immagine 2',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
    )

    image3 = forms.ImageField(
        label='Immagine 3',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
    )

    image4 = forms.ImageField(
        label='Immagine 4',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
    )

    image5 = forms.ImageField(
        label='Immagine 5',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Categorie'
    )


    class Meta:
        model = Product
        fields = ['title', 'description', 'image1', 'image2', 'image3', 'image4', 'image5', 'price', 'quantity', 'categories']

