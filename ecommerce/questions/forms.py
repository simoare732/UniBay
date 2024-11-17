from django import forms
from .models import Question

class question_create_form(forms.ModelForm):
    text = forms.CharField(
        label='Domanda',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Question
        fields = ['text']