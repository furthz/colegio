from django import forms
from django.forms import ModelForm
from payments.models import TipoPago
from payments.models import Pago
from django.utils.translation import ugettext_lazy as _

class TipoPagoForm(forms.ModelForm):
    class Meta:
        model = TipoPago

        fields = [

            'colegio',
            'descripcion',
            'tipo',
            'padre',
            'eliminado',
        ]

        labels = {

            'colegio': 'Colegio',
            'descripcion': 'Descripción',
            'tipo': 'Tipo',
            'padre': 'Padre',
            'eliminado': 'Eliminado',
        }

        widgets = {

            'colegio': forms.Select(attrs={'class': 'hidden'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'tipo': forms.TextInput(attrs={'class': 'hidden', 'id': 'describe', 'name': 'lname'}),
            'padre': forms.Select(attrs={'class': 'form-control'}),
            'eliminado': forms.CheckboxInput(),
        }



class PagoForm(ModelForm):

    class Meta:
        model = Pago

        fields = [
            'proveedor',
            'tipo_pago',
            'descripcion',
            'monto',
            'numero_comprobante',
        ]

        labels = {

            'proveedor':_('Proveedor'),
            'tipo_pago':_('Tipo de Pago'),
            'descripcion':_('Descripción'),
            'monto':_('Monto'),
            'numero_comprobante':_('Nro Comprobante'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_pago'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})
        self.fields['monto'].widget.attrs.update({'class': 'form-control'})
        self.fields['numero_comprobante'].widget.attrs.update({'class': 'form-control'})