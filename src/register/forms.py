from profiles.models import Profile
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm, SelectDateWidget

from register.models import Alumno, Apoderado
from utils.forms import ValidProfileFormMixin
from utils.models import TipoDocumento, TipoSexo


class PersonaForm(ModelForm):

    @property
    def ChoiceTipoDocumento(self):
        choices = [(tipo.id_tipo, tipo.descripcion) for tipo in TipoDocumento.objects.all()]
        return choices

    @property
    def ChoiceTipoSexo(self):
        choices = [(sex.id_sexo, sex.descripcion) for sex in TipoSexo.objects.all()]
        return choices

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_documento'] = forms.ChoiceField(choices=self.ChoiceTipoDocumento)
        self.fields['sexo'] = forms.ChoiceField(choices=self.ChoiceTipoSexo)
        self.fields['fecha_nac'] = forms.DateField(widget=SelectDateWidget(
            empty_label=("Elige Año", "Elige Mes", "Elige Día")))

    class Meta:
        model = Profile
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class AlumnoForm(ValidProfileFormMixin, PersonaForm):

    class Meta:
        model = Alumno
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']
        labels = {
            'nombre': _('Nombre'),
            'segundo_nombre': _('Segundo Nombre'),
            'apellido_ma': _('Apellido Materno'),
            'apellido_pa': _('Apellido Paterno'),
            'tipo_documento': _('Tipo Documento'),
            'numero_documento': _('Número Documento'),
            'sexo': _('Sexo'),
            'correo': _('Correo'),
            'fecha_nac': _('Fecha Nac.'),
        }


class ApoderadoForm(ValidProfileFormMixin, PersonaForm):

    class Meta:
        model = Apoderado
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'parentesco', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']
        labels = {
            'nombre': _('Nombre'),
            'segundo_nombre': _('Segundo Nombre'),
            'apellido_ma': _('Apellido Materno'),
            'apellido_pa': _('Apellido Paterno'),
            'parentesco': _('Parentesco'),
            'tipo_documento': _('Tipo Documento'),
            'numero_documento': _('Número Documento'),
            'sexo': _('Sexo'),
            'correo': _('Correo'),
            'fecha_nac': _('Fecha Nac.'),
        }

