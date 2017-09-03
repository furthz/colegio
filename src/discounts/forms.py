from django import forms
from enrollment.models import Servicio
from enrollment.models import TipoServicio
from enrollment.models import Matricula
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, Form
from utils.models import TiposNivel
from django.utils.translation import ugettext_lazy as _
from discounts.models import Descuento
from discounts.models import TipoDescuento

##############################################################
#       Solicitar Descuentos
##############################################################

class SolicitarDescuentoForm(ModelForm):
    """
    Formulario de la clase Descuento
    Nota:
        solo se añade como campos los que son definidos por los usuarios
    """
    class Meta:
        model = Descuento
        fields = [
            'matricula',
            'tipo_descuento',
            'numero_expediente',
            'comentario',
        ]
        labels = {
            'matricula':_('Solicitante'),
            'tipo_descuento':_('Descuento'),
            'numero_expediente':_('Nro. Expediente'),
            'comentario':_('Comentario'),
        }

    def ChoiceNiveles(self):
        MY_CHOICES = (
            ('1', 'Inicial'),
            ('2', 'Primaria'),
            ('3', 'Secundaria'),
        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['nivel'] = forms.ChoiceField(choices=self.ChoiceNiveles())
        #self.fields['grado'] = forms.ChoiceField(choices=self.ChoiceGrados())
        self.fields['matricula'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_descuento'].widget.attrs.update({'class': 'form-control'})
        self.fields['numero_expediente'].widget.attrs.update({'class': 'form-control'})
        self.fields['comentario'].widget.attrs.update({'class': 'form-control'})
        self.fields['matricula'].widget.attrs['editable'] = False





##############################################################
#       Aprobar Descuentos
##############################################################
