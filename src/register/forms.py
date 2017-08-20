from profiles.models import Profile
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm, SelectDateWidget

from register.models import Alumno
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


class AlumnoForm(PersonaForm):


    def is_valid(self):
        valid = super(AlumnoForm, self).is_valid()

        try:
            persona_registrada = Profile.objects.get(numero_documento=self.cleaned_data["numero_documento"],
                                                 tipo_documento=self.cleaned_data["tipo_documento"])

            if (persona_registrada.apellido_pa.upper() != self.cleaned_data["apellido_pa"].upper()) \
                    and (persona_registrada.apellido_ma.upper() != self.cleaned_data["apellido_ma"].upper()):
                self.add_error('numero_documento', 'La persona a ingresar no coincide con el ya existente, '
                                                   'verifique el número de documento ingresado '
                                                   'la persona ya registrada es: ' + persona_registrada.getNombreCompleto.title())
                valid = False

        except Profile.DoesNotExist:
            persona_registrada = None




        return valid


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
        #labels = ['Nombre', 'Segundo Nombre', 'Apellido Paterno', 'Apellido Materno', 'Tipo Documento',
        #          'Número Documento', 'Sexo', 'Correo', 'Fec. Nac.']


