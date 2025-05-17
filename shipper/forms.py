# shipper/forms.py
from django import forms
from .models import Freight, Shipper

class FreightCreateForm(forms.ModelForm):
    class Meta:
        model = Freight
        fields = ['name', 'trailer', 'mass', 'status', 'offered_price', 'location']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Freight Name'
            }),
            'trailer': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Trailer (m)'
            }),
            'location': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select Location'
            }),
            'mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'offered_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price per km',
                'step': '0.01'
            }),
        }
        labels = {
            'offered_price': 'Price per km ($)'
        }