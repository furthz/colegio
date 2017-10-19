
from django import forms
from AE_academico.models import Aula, Asistencia, Notas, Curso
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


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso

        fields = [
            'aula',
            'nombre',
            'descripcion',
        ]

        labels = {
            'aula': 'Aula',
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
        }

        widgets = {
            'aula': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
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

class MarcarAsistenciaForm(forms.Form):

    estado_asistencia = forms.BooleanField()

    def ChoiceEstado(self):
        MY_CHOICES = (
            (True, 'Presente'),
            (False, 'Ausente'),
        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado_asistencia'] = forms.ChoiceField(choices=self.ChoiceEstado())
        self.fields['estado_asistencia'].widget.attrs.update({'class': 'form-control'})

class SubirNotasForm(forms.Form):

    nota = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nota'].widget.attrs.update({'class': 'form-control'})
