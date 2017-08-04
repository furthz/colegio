from django import forms
from enrollment.models import Servicio
from enrollment.models import TipoServicio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

class TipoServicioForm(ModelForm):
    """
    Formulario de la clase TipoServicio
    Nota:
        solo se añade como campos los que son definidos por los usuarios
    """
    class Meta:
        model = TipoServicio
        fields = ['is_ordinario','nivel','grado','extra','codigo_modular']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Save'))



class ServicioForm(ModelForm):
    """
    Formulario de la clase Servicio
    Nota:
        solo se añaden com campos los que son definidos por los usuarios
    """
    class Meta:
        model = Servicio
        fields = ['nombre','precio','is_periodic','fecha_facturar','cuotas']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Save'))
