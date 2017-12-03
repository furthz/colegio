
from django import forms
from AE_academico.models import Aula, Asistencia, Notas, Curso, Evento, PeriodoAcademico, HorarioAula, RecordatorioAula
from AE_academico.models import CursoDocente
from utils.middleware import get_current_colegio


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
            'nombre',
            'descripcion',
        ]

        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
        }

        widgets = {
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

    estado_asistencia = forms.IntegerField()

    def ChoiceEstado(self):
        MY_CHOICES = (
            (1, '-------'),
            (2, 'Presente'),
            (3, 'Ausente'),
            (4, 'Tardanza'),
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


class RegistrarNotas2Form(forms.Form):

    nota = forms.CharField(max_length=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nota'].widget.attrs.update({'class': 'form-control'})


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento

        fields = [
            'nombre',
            'encargado',
            'descripcion',
            'fecha_evento',
            'hora_inicio',
            'hora_fin',
        ]

        labels = {
            'nombre':'Nombre',
            'encargado': 'Responsable',
            'descripcion': 'Descripcion del Evento',
            'fecha_evento': 'Fecha del Evento',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Fin',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['encargado'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_evento'].widget.attrs.update({'class': 'form-control'})
        self.fields['hora_inicio'].widget.attrs.update({'class': 'form-control'})
        self.fields['hora_fin'].widget.attrs.update({'class': 'form-control'})


class PeriodoAcademicoForm(forms.ModelForm):
    class Meta:
        model = PeriodoAcademico
        fields = ['nombre', 'fecha_inicio', 'fecha_fin']


class HorarioAulaForm(forms.ModelForm):
    class Meta:
        model = HorarioAula

        fields = [
            'curso',
            'lugar',
            'dia',
            'hora_inicio',
            'hora_fin',
        ]

        labels = {
            'curso':'Curso',
            'lugar': 'Lugar',
            'dia': 'Día',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Fin',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['curso'].widget.attrs.update({'class': 'form-control'})
        self.fields['lugar'].widget.attrs.update({'class': 'form-control'})
        self.fields['dia'].widget.attrs.update({'class': 'form-control'})
        self.fields['hora_inicio'].widget.attrs.update({'class': 'form-control'})
        self.fields['hora_fin'].widget.attrs.update({'class': 'form-control'})

class RecordatorioAulaForm(forms.ModelForm):
    class Meta:
        model = RecordatorioAula

        fields = [
            'nombre',
            'descripcion',
            'fecha_programacion'
        ]

        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'fecha_programacion': 'Fecha'
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_programacion': forms.TextInput(attrs={'class': 'form-control'}),
        }
