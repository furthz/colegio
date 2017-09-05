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
from utils.middleware import get_current_colegio, get_current_userID

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


class TipoDescuentForm(ModelForm):
    """
        Formulario de la clase Descuento
        Nota:
            solo se añade como campos los que son definidos por los usuarios
        """
    servicio = forms.ModelChoiceField(queryset=Servicio.objects.filter(activo=True))
    class Meta:
        model = TipoDescuento
        fields = [
            'servicio',
            'descripcion',
            'porcentaje',
        ]
        labels = {
            'servicio': _('Servicio'),
            'descripcion': _('Descripción'),
            'porcentaje': _('Porcentaje'),
        }



    def __init__(self, *args, **kwargs):
        colegio = kwargs.pop('colegio', None)
        super(TipoDescuentForm, self).__init__(*args, **kwargs)
        # self.fields['nivel'] = forms.ChoiceField(choices=self.ChoiceNiveles())
        # self.fields['grado'] = forms.ChoiceField(choices=self.ChoiceGrados())
        self.fields['servicio'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})
        self.fields['porcentaje'].widget.attrs.update({'class': 'form-control'})

        if colegio:
            self.fields['servicio'].queryset = Servicio.objects.filter(activo=True,tipo_servicio__colegio__id_colegio=colegio)

##############################################################
#       Aprobar Descuentos
##############################################################

class DetalleDescuentosForm(forms.Form):
    """
    Formulario para filtar los detalles de Control de ingresos
    Nota:
        solo se añaden com campos los que son definidos por los usuarios
    """

    alumno = forms.CharField(required=False)
    anio = forms.CharField()
    numero_expediente = forms.CharField(required=False)
    estado = forms.CharField()

    def ChoiceAnio(self):
        MY_CHOICES = (
            ('2017', '2017'),
            ('2016', '2016'),
        )
        return MY_CHOICES

    def ChoiceEstado(self):
        MY_CHOICES = (
            ('Todos', 'Todos'),
            ('Aprobado', 'Aprobado'),
            ('No_aprobado', 'No aprobado'),
            ('Pendiente', 'Pendiente'),
        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anio'] = forms.ChoiceField(choices=self.ChoiceAnio())
        self.fields['estado'] = forms.ChoiceField(choices=self.ChoiceEstado())
        self.fields['alumno'].widget.attrs.update({'class': 'form-control'})
        self.fields['anio'].widget.attrs.update({'class': 'form-control'})
        self.fields['numero_expediente'].widget.attrs.update({'class': 'form-control'})
        self.fields['estado'].widget.attrs.update({'class': 'form-control'})
