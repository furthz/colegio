from django import forms
from enrollment.models import Servicio
from enrollment.models import TipoServicio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from utils.models import TiposNivel

class TipoServicioForm(ModelForm):
    """
    Formulario de la clase TipoServicio
    Nota:
        solo se añade como campos los que son definidos por los usuarios
    """
    class Meta:
        model = TipoServicio
        fields = ['is_ordinario','nivel','grado','extra','codigo_modular']
    def ChoiceNiveles(self):
        MY_CHOICES = (
            ('1', 'Inicial'),
            ('2', 'Primaria'),
            ('3', 'Secundaria'),
        )
        return MY_CHOICES

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
        #self.fields['nivel'] = forms.ChoiceField(choices=self.ChoiceNiveles(),initial=1)
        #self.fields['grado'] = forms.ChoiceField(choices=self.ChoiceGrados())


class ServicioForm(ModelForm):
    """
    Formulario de la clase Servicio
    Nota:
        solo se añaden com campos los que son definidos por los usuarios
    """
    class Meta:
        model = Servicio
        fields = ['nombre','precio','is_periodic','fecha_facturar','cuotas']

    def ChoiceServicios(self):
        MY_CHOICES = (
            ('Matricula', 'Matricula'),
            ('Pension', 'Pensión'),
        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'] = forms.ChoiceField(choices=self.ChoiceServicios())
