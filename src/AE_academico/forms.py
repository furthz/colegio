"""
from django import forms
from AE_academico.models import Aula
from AE_academico.models import CursoDocente

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula

        fields = [
            'tipo_servicio',
            'nombre',
        ]

        labels = {
            'tipo_servicio': 'Nivel y Grado',
            'nombre': 'Nombre',
        }

        widgets = {
            'tipo_servicio': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CursoDocenteForm(forms.ModelForm):
    class Meta:
        model = CursoDocente

        fields = [
            'docente',
            'curso',
        ]

        labels = {
            'docente': 'Docente',
            'curso': 'Curso',
        }

        widgets = {
            'docente': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
        }
"""
