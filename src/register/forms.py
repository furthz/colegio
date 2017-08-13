from profiles.models import Profile

from django import forms
from django.forms import ModelForm, SelectDateWidget

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
