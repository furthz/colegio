from django import forms
from django.forms import ModelForm
from payments.models import TipoPago
from payments.models import Pago
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper

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
        self.fields['proveedor'].widget.attrs.update({'class': 'form-control select2'})
        self.fields['tipo_pago'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})
        self.fields['monto'].widget.attrs.update({'class': 'form-control'})
        self.fields['numero_comprobante'].widget.attrs.update({'class': 'form-control'})


class ControlPagosPromotorForm(forms.Form):
    """
    Formulario para filtar los detalles de Control de pagos
    Nota:
        solo se añaden com campos los que son definidos por los usuarios
    """
    tipo_pago = forms.ModelChoiceField(
        label='Tipo_pago',
        queryset=None,
        required=False, )

    anio = forms.CharField()
    mes = forms.CharField()
    fecha_inicio = forms.DateField()
    fecha_final = forms.DateField()

    def ChoiceAnio(self):
        MY_CHOICES = (
            ('2017', '2017'),
            ('2016', '2016'),
        )
        return MY_CHOICES

    def ChoiceMes(self):
        MY_CHOICES = (
            ('Todos', 'Todos'),
            ('Enero', 'Enero'),
            ('Febrero', 'Febrero'),
            ('Marzo', 'Marzo'),
            ('Abril', 'Abril'),
            ('Mayo', 'Mayo'),
            ('Junio', 'Junio'),
            ('Julio', 'Julio'),
            ('Agosto', 'Agosto'),
            ('Setiembre', 'Setiembre'),
            ('Octubre', 'Octubre'),
            ('Noviembre', 'Noviembre'),
            ('Diciembre', 'Diciembre'),
        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anio'] = forms.ChoiceField(choices=self.ChoiceAnio())
        self.fields['anio'].widget.attrs.update({'class': 'form-control'})
        self.fields['mes'] = forms.ChoiceField(choices=self.ChoiceMes())
        self.fields['mes'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_pago'].widget.attrs.update({'class': 'form-control'})

        tipos = TipoPago.objects.all()
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.fields['tipo_pago'].queryset = tipos
