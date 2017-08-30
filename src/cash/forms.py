from django import forms
from .models import Caja, CajaCajero, Remesa



class CashierForm(forms.ModelForm):
    class Meta:
        model = Caja

        fields = [
            'colegio',
            'numero',
            'descripcion',
            'activo',
            'eliminado',
            'fecha_creacion',
            'fecha_modificacion',
            'usuario_creacion',
            'usuario_modificacion',
        ]

        labels = {
            'colegio': 'Colegio',
            'numero': 'Número de Caja',
            'descripcion': 'Descripción',
            'activo': 'Activo',
            'eliminado': 'Eliminado',
            'fecha_creacion': 'Fecha de Creación',
            'fecha_modificacion': 'Fecha de Modificación',
            'usuario_creacion': 'Usuario creación',
            'usuario_modificacion': 'Usuario Modificación',
        }

        widgets = {

            'colegio': forms.Select(attrs={'class': 'hidden'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(),
            'eliminado': forms.CheckboxInput(),
            'fecha_creacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_modificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_creacion': forms.HiddenInput(attrs={'class': 'form-control'}),
            'usuario_modificacion': forms.HiddenInput(attrs={'class': 'form-control'}),
        }


class BoxCashierForm(forms.ModelForm):
    class Meta:
        model = CajaCajero

        fields = [
            'personal_colegio',
            'caja',
            'saldo',
            'monto_apertura',
            'monto_cierre',
            'comentario_apertura',
            'comentario_cierre',
            'estado',
            'fecha_creacion',
            'fecha_modificacion',
            'usuario_creacion',
            'usuario_modificacion',
        ]

        labels = {
            'personal_colegio': 'Cajero',
            'caja': 'N° de Caja',
            'saldo': 'Saldo',
            'monto_apertura': 'Monto de Apertura',
            'monto_cierre': 'Monto de Cierre',
            'comentario_apertura': 'Comentario Apertura',
            'comentario_cierre': 'Comentario Cierre',
            'estado': 'Estado',
            'fecha_creacion': 'Fecha de Creación',
            'fecha_modificacion': 'Fecha de Modificación',
            'usuario_creacion': 'Usuario de Creación',
            'usuario_modificacion': 'Usuario de Modificación',
        }

        widgets = {

            'personal_colegio': forms.Select(attrs={'class': 'hidden'}),
            'caja': forms.Select(attrs={'class': 'form-control'}),
            'saldo': forms.TextInput(attrs={'class': 'form-control'}),
            'monto_apertura': forms.TextInput(attrs={'class': 'form-control'}),
            'monto_cierre': forms.TextInput(attrs={'class': 'form-control'}),
            'comentario_apertura': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'comentario_cierre': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'estado': forms.CheckboxInput(attrs={'id': 'Uncheck'}),
            'fecha_creacion': forms.HiddenInput(attrs={'class': 'form-control'}),
            'fecha_modificacion': forms.HiddenInput(attrs={'class': 'form-control'}),
            'usuario_creacion': forms.HiddenInput(attrs={'class': 'form-control'}),
            'usuario_modificacion': forms.HiddenInput(attrs={'class': 'form-control'}),
        }


class ConsignmentForm(forms.ModelForm):
    class Meta:
        model = Remesa

        fields = [
            'personal_colegio',
            'movimiento',
            'fechacreacion',
            'monto',
            'comentario',
        ]

        labels = {
            'personal_colegio': 'Persona Encargada',
            'movimiento': 'Cajero',
            'fechacreacion': 'Fecha Creación',
            'monto': 'Monto',
            'comentario': 'Comentario',
        }

        widgets = {

            'personal_colegio': forms.Select(attrs={'class': 'form-control', 'id': 'personaTxt', 'name': 'personaTxt',
                                                    'onchange': 'personaSelect()'}),
            'movimiento': forms.Select(attrs={'class': 'form-control'}),
            'fechacreacion': forms.HiddenInput(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(
                attrs={'class': 'form-control', 'name': 'inputMonto', 'onKeyPress': 'return soloNumeros(event)',
                       'placeholder': 'Escribe el monto a entregar',
                       "onchange": "document.getElementById('monto').innerHTML = montodine = this.value"}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }
