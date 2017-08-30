from django import forms
from .models import TipoPago


class TipoPagoForm(forms.ModelForm):
    class Meta:
        model = TipoPago

        fields = [

            'descripcion',
            'padre',
            'eliminado',
        ]

        labels = {

            'descripcion': 'Descripción',
            'padre': 'Padre',
            'eliminado': 'Eliminado',
        }

        widgets = {

            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'padre': forms.Select(attrs={'class': 'form-control'}),
            'eliminado': forms.CheckboxInput(),
        }
