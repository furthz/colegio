# coding=utf-8
from django import forms
from .models import *
from django.db.models import Count


class TipoAlertaForm(forms.ModelForm):
    class Meta:
        model = TipoAlerta

        fields = [
            'descripcion',
            'fecha_creacion',
            'fecha_modificacion',
        ]

        labels = {
            'descripcion': 'Descripción',
            'fecha_creacion': 'Fecha de Creación',
            'fecha_modificacion': 'Fecha de Modificación',
        }

        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'tabindex': '2'}),
            'fecha_creacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_modificacion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EstadoAlertaForm(forms.ModelForm):
    class Meta:
        model = EstadoAlerta

        fields = [
            'descripcion',
            'fecha_creacion',
            'fecha_modificacion',
        ]

        labels = {
            'descripcion': 'Descripción',
            'fecha_creacion': 'Fecha de Creación',
            'fecha_modificacion': 'Fecha de Modificación',
        }

        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'tabindex': '2'}),
            'fecha_creacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_modificacion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ContenidoAlertatForm(forms.ModelForm):
    class Meta:
        model = ContenidoAlerta

        fields = [
            'contenido',
        ]

        labels = {
            'contenido': 'Contenido',
        }

        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'tabindex': '2'}),
        }

class PersonaEmisorForm(forms.ModelForm):
    class Meta:
        model = PersonaEmisor

        fields = [
            'profile',
        ]

        labels = {
            'profile': 'Emisor',
        }

        widgets = {
            'profile': forms.Select(attrs={'class': 'form-control', 'tabindex': '1'}),
        }


class PersonaReceptorForm(forms.ModelForm):
    class Meta:
        model = PersonaReceptor

        fields = [
            'profile',
        ]

        labels = {
            'profile': 'Receptor',
        }

        widgets = {
            'profile': forms.Select(attrs={'class': 'form-control', 'tabindex': '1'}),
        }

class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta

        fields = [
            'matricula',
            'persona_emisor',
            'persona_receptor',
            'tipo_alerta',
            'estado_alerta',
            'contenido_alerta',
            'fecha_visto',
            'visto',

        ]

        labels = {
            'matricula': 'Matricula',
            'persona_emisor': 'Emisor',
            'persona_receptor': 'Receptor',
            'tipo_alerta': 'Tipo Alerta',
            'estado_alerta': 'Estado Alerta',
            'contenido_alerta': 'Contenido Alerta',
            'fecha_visto': 'Fecha Visto',
            'visto': 'Visto',

        }

        widgets = {

            'matricula': forms.Select(attrs={'class': 'form-control'}),
            'persona_emisor': forms.Select(attrs={'class': 'form-control'}),
            'persona_receptor': forms.Select(attrs={'class': 'form-control'}),
            'tipo_alerta': forms.Select(attrs={'class': 'form-control'}),
            'estado_alerta': forms.Select(attrs={'class': 'form-control'}),
            'contenido_alerta': forms.Select(attrs={'class': 'form-control'}),
            'fecha_visto': forms.TextInput(attrs={'class': 'form-control'}),
            'visto': forms.TextInput(attrs={'class': 'form-control'}),
        }