from django import forms
from enrollment.models import Servicio
from enrollment.models import TipoServicio
from enrollment.models import Matricula
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
        widgets = {
            'nivel': forms.RadioSelect(attrs={'class':'form-control'}),
                   }


    def ChoiceNiveles(self):
        MY_CHOICES = (
            ('1', 'Inicial'),
            ('2', 'Primaria'),
            ('3', 'Secundaria'),
        )
        return MY_CHOICES

    def ChoiceGrados(self):
        MY_CHOICES = (
            ('1', '3 Años'),
            ('2', '4 Años'),
            ('3', '5 Años'),
            ('4', '1er Grado'),
            ('5', '2do Grado'),
            ('6', '3er Grado'),
            ('7', '4to Grado'),
            ('8', '5to Grado'),
            ('9', '6to Grado'),

        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nivel'] = forms.ChoiceField(choices=self.ChoiceNiveles(),initial=1)
        self.fields['grado'] = forms.ChoiceField(choices=self.ChoiceGrados())
        self.fields['nivel'].widget.attrs.update({'class': 'form-control'})
        self.fields['grado'].widget.attrs.update({'class': 'form-control'})
        self.fields['extra'].widget.attrs.update({'class': 'form-control'})


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
        self.h


class MatriculaForm(ModelForm):
    class Meta:
        model = Matricula
        fields = ['alumno','tipo_servicio']



    #def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        #self.fields['nombre'] = forms.ChoiceField(choices=self.ChoiceServicios())


