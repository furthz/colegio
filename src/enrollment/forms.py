from django import forms
from enrollment.models import Servicio
from enrollment.models import TipoServicio
from enrollment.models import Matricula
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from utils.models import TiposNivel
from utils.models import TiposGrados
from django.utils.translation import ugettext_lazy as _



class TipoServicioRegularForm(ModelForm):
    """
    Formulario de la clase TipoServicio
    Nota:
        solo se añade como campos los que son definidos por los usuarios
    """
    class Meta:
        model = TipoServicio
        fields = ['nivel','grado','codigo_modular']
        labels = {
            'nivel':_('Nivel'),
            'grado':_('Grado/Seccion'),
            'codigo_modular':_('Codigo Modular'),
        }

    def ChoiceNiveles(self):
        choices = [(d.id_tipo, d.descripcion) for d in TiposNivel.objects.all()]
        return choices

    def ChoiceGrados(self):
        choices = [(d.id_tipo_grado, d.descripcion) for d in TiposGrados.objects.all()]
        return choices


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nivel'] = forms.ChoiceField(choices=self.ChoiceNiveles())
        self.fields['grado'] = forms.ChoiceField(choices=self.ChoiceGrados())
        self.fields['nivel'].widget.attrs.update({'class': 'form-control'})
        self.fields['grado'].widget.attrs.update({'class': 'form-control'})
        self.fields['codigo_modular'].widget.attrs.update({'class': 'form-control'})

class TipoServicioExtraForm(ModelForm):
    """
    Formulario de la clase TipoServicio
    Nota:
        solo se añade como campos los que son definidos por los usuarios
    """
    extra = forms.CharField(label='Extracurricular')
    class Meta:
        model = TipoServicio
        fields = ['extra']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['extra'].widget.attrs.update({'class': 'form-control'})


class ServicioRegularForm2(ModelForm):
    """
    Formulario de la clase Servicio
    Nota:
        solo se añaden com campos los que son definidos por los usuarios
    """

    class Meta:
        model = Servicio
        fields = ['tipo_servicio', 'nombre', 'precio', 'fecha_facturar']
        labels = {
            'tipo_servicio': _('Nivel/Grado'),
            'nombre': _('Concepto de Pago'),
            'precio': _('Precio'),

            'fecha_facturar': _("Día de inicio de generación de la deuda"),
        }

    def ListaConceptoPago(self):
        MY_CHOICES = (
            ('Matricula', 'Matricula'),
            ('Pension', 'Pensión'),
            ('Cuota de Ingreso', 'Cuota de Ingreso'),
        )
        return MY_CHOICES

    def ListadeMeses(self):
        MY_CHOICES = (
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (6, '6'),
            (7, '7'),
            (8, '8'),
            (9, '9'),
            (10, '10'),
            (11, '11'),
            (12, '12'),
        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'] = forms.ChoiceField(choices=self.ListaConceptoPago())

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})

        self.fields['tipo_servicio'].widget.attrs.update({'class': 'form-control'})
        self.fields['precio'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_facturar'].widget.attrs.update({'tabindex': '8', 'class': 'form-control'})


class ServicioRegularForm(ModelForm):
    """
    Formulario de la clase Servicio
    Nota:
        solo se añaden com campos los que son definidos por los usuarios
    """

    class Meta:
        model = Servicio
        fields = ['tipo_servicio','nombre','precio','fecha_facturar','cuotas']
        labels = {
            'tipo_servicio': _('Nivel/Grado'),
            'nombre': _('Concepto de Pago'),
            'precio': _('Precio'),
            'cuotas': _('Nro. de Meses'),
            'fecha_facturar': _("Día de inicio de generación de la deuda"),
        }
    def ListaConceptoPago(self):
        MY_CHOICES = (
            ('Matricula', 'Matricula'),
            ('Pension', 'Pensión'),
            ('Cuota de Ingreso','Cuota de Ingreso'),
        )
        return MY_CHOICES
    def ListadeMeses(self):
        MY_CHOICES = (
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (6, '6'),
            (7, '7'),
            (8, '8'),
            (9, '9'),
            (10, '10'),
            (11, '11'),
            (12, '12'),
        )
        return MY_CHOICES
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'] = forms.ChoiceField(choices=self.ListaConceptoPago())
        self.fields['cuotas'] = forms.ChoiceField(choices=self.ListadeMeses())
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['cuotas'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_servicio'].widget.attrs.update({'class': 'form-control'})
        self.fields['precio'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_facturar'].widget.attrs.update({'tabindex': '8','class': 'form-control'})

class ServicioExtraCreateForm(ModelForm):
    """
    Formulario de la clase Servicio
    Nota:
        solo se añaden com campos los que son definidos por los usuarios
    """

    class Meta:
        model = Servicio
        fields = ['tipo_servicio','nombre','precio','fecha_facturar']
        labels = {
            'tipo_servicio': _('Extracurricular'),
            'nombre': _('Concepto de Pago'),
            'precio': _('Precio'),

            'fecha_facturar': _("Día de inicio de generacion de la deuda"),
        }
    def ListaConceptoPago(self):
        MY_CHOICES = (
            ('Matricula', 'Matricula'),
            ('Pension', 'Pensión'),
            ('Cuota de Ingreso','Cuota de Ingreso'),
        )
        return MY_CHOICES
    def ListadeMeses(self):
        MY_CHOICES = (
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (6, '6'),
            (7, '7'),
            (8, '8'),
            (9, '9'),
            (10, '10'),
            (11, '11'),
            (12, '12'),
        )
        return MY_CHOICES
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'] = forms.ChoiceField(choices=self.ListaConceptoPago())
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_servicio'].widget.attrs.update({'class': 'form-control'})
        self.fields['precio'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_facturar'].widget.attrs.update({'class': 'form-control'})


class ServicioExtraForm(ModelForm):
    """
    Formulario de la clase Servicio
    Nota:
        solo se añaden com campos los que son definidos por los usuarios
    """

    class Meta:
        model = Servicio
        fields = ['tipo_servicio','nombre','precio','fecha_facturar','cuotas']
        labels = {
            'tipo_servicio': _('Extracurricular'),
            'nombre': _('Concepto de Pago'),
            'precio': _('Precio'),
            'cuotas': _('Nro. de Meses'),
            'fecha_facturar': _("Día de inicio de generacion de la deuda"),
        }
    def ListaConceptoPago(self):
        MY_CHOICES = (
            ('Matricula', 'Matricula'),
            ('Pension', 'Pensión'),
            ('Cuota de Ingreso','Cuota de Ingreso'),
        )
        return MY_CHOICES
    def ListadeMeses(self):
        MY_CHOICES = (
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (6, '6'),
            (7, '7'),
            (8, '8'),
            (9, '9'),
            (10, '10'),
            (11, '11'),
            (12, '12'),
        )
        return MY_CHOICES
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'] = forms.ChoiceField(choices=self.ListaConceptoPago())
        self.fields['cuotas'] = forms.ChoiceField(choices=self.ListadeMeses())
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['cuotas'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_servicio'].widget.attrs.update({'class': 'form-control'})
        self.fields['precio'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_facturar'].widget.attrs.update({'class': 'form-control'})

class MatriculaForm(ModelForm):
    class Meta:
        model = Matricula
        fields = ['alumno','tipo_servicio']



    #def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        #self.fields['nombre'] = forms.ChoiceField(choices=self.ChoiceServicios())


