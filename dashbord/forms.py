from django import forms
from .models import RecognizedAlphabet


class RecognizedAlphabetForm(forms.ModelForm):
    class Meta:
        model = RecognizedAlphabet
        fields = ['pdf_file']
