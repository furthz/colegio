from django import forms
from crispy_forms.helper import FormHelper
from register.models import Apoderado, Profile
import logging
from utils.middleware import get_current_user

logger = logging.getLogger("project")

class CuentasCobrarPromotorForm(forms.Form):
    """
    Formulario para filtar los detalles de Control de ingresos
    Nota:
        solo se añaden com campos los que son definidos por los usuarios
    """

    anio = forms.CharField()
    mes = forms.CharField()

    def ChoiceAnio(self):
        MY_CHOICES = (
            ('2017', '2017'),
            ('2016', '2016'),
        )
        return MY_CHOICES

    def ChoiceMes(self):
        MY_CHOICES = (
            ('Todos', 'Todos'),
            ('Enero', 'Enero'),
            ('Febrero', 'Febrero'),
            ('Marzo', 'Marzo'),
            ('Abril', 'Abril'),
            ('Mayo', 'Mayo'),
            ('Junio', 'Junio'),
            ('Julio', 'Julio'),
            ('Agosto', 'Agosto'),
            ('Setiembre', 'Setiembre'),
            ('Octubre', 'Octubre'),
            ('Noviembre', 'Noviembre'),
            ('Diciembre', 'Diciembre'),
        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anio'] = forms.ChoiceField(choices=self.ChoiceAnio())
        self.fields['mes'] = forms.ChoiceField(choices=self.ChoiceMes())
        self.fields['anio'].widget.attrs.update({'class': 'form-control'})
        self.fields['mes'].widget.attrs.update({'class': 'form-control'})


class CuentasCobrarPromotorDetalleForm(forms.Form):
    """
    Formulario para filtar los detalles de Control de ingresos
    Nota:
        solo se añaden com campos los que son definidos por los usuarios
    """

    alumno = forms.CharField()
    anio = forms.CharField()
    mes = forms.CharField()
    estado = forms.CharField()

    def ChoiceAnio(self):
        MY_CHOICES = (
            ('Todos', 'Todos'),
            ('2017', '2017'),
            ('2016', '2016'),
        )
        return MY_CHOICES

    def ChoiceMes(self):
        MY_CHOICES = (
            ('Todos', 'Todos'),
            ('Enero', 'Enero'),
            ('Febrero', 'Febrero'),
            ('Marzo', 'Marzo'),
            ('Abril', 'Abril'),
            ('Mayo', 'Mayo'),
            ('Junio', 'Junio'),
            ('Julio', 'Julio'),
            ('Agosto', 'Agosto'),
            ('Setiembre', 'Setiembre'),
            ('Octubre', 'Octubre'),
            ('Noviembre', 'Noviembre'),
            ('Diciembre', 'Diciembre'),
        )
        return MY_CHOICES

    def ChoiceEstado(self):
        MY_CHOICES = (
            ('Todos', 'Todos'),
            ('Pagado', 'Pagado'),
            ('No_pagado', 'No pagado'),
        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anio'] = forms.ChoiceField(choices=self.ChoiceAnio())
        self.fields['mes'] = forms.ChoiceField(choices=self.ChoiceMes())
        self.fields['estado'] = forms.ChoiceField(choices=self.ChoiceEstado())
        self.fields['alumno'].widget.attrs.update({'class': 'form-control'})
        self.fields['anio'].widget.attrs.update({'class': 'form-control'})
        self.fields['mes'].widget.attrs.update({'class': 'form-control'})
        self.fields['estado'].widget.attrs.update({'class': 'form-control'})

class CuentasCobrarPadresForm(forms.Form):

    alumno = forms.ModelChoiceField(
        label='Alumnos',
        queryset=None,
        required=True, )

    anio = forms.CharField()
    mes = forms.CharField()
    estado = forms.CharField()

    def ChoiceAnio(self):
        MY_CHOICES = (
            ('Todos', 'Todos'),
            ('2017', '2017'),
            ('2016', '2016'),
        )
        return MY_CHOICES

    def ChoiceMes(self):
        MY_CHOICES = (
            ('Todos', 'Todos'),
            ('Enero', 'Enero'),
            ('Febrero', 'Febrero'),
            ('Marzo', 'Marzo'),
            ('Abril', 'Abril'),
            ('Mayo', 'Mayo'),
            ('Junio', 'Junio'),
            ('Julio', 'Julio'),
            ('Agosto', 'Agosto'),
            ('Setiembre', 'Setiembre'),
            ('Octubre', 'Octubre'),
            ('Noviembre', 'Noviembre'),
            ('Diciembre', 'Diciembre'),
        )
        return MY_CHOICES

    def ChoiceEstado(self):
        MY_CHOICES = (
            ('Todos', 'Todos'),
            ('Pagado', 'Pagado'),
            ('No_pagado', 'No pagado'),
        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anio'] = forms.ChoiceField(choices=self.ChoiceAnio())
        self.fields['mes'] = forms.ChoiceField(choices=self.ChoiceMes())
        self.fields['estado'] = forms.ChoiceField(choices=self.ChoiceEstado())
        self.fields['alumno'].widget.attrs.update({'class': 'form-control'})
        self.fields['anio'].widget.attrs.update({'class': 'form-control'})
        self.fields['mes'].widget.attrs.update({'class': 'form-control'})
        self.fields['estado'].widget.attrs.update({'class': 'form-control'})

        user = get_current_user()
        logger.debug("Usuario: " + user.name)

        profile = Profile.objects.get(user=user)
        logger.debug("profile: " + str(profile.id_persona))

        apoderado = Apoderado.objects.get(persona=profile)
        logger.debug("apoderado: " + str(apoderado.id_apoderado))

        alumnos = apoderado.alumnos.all()

        self.helper = FormHelper()
        self.helper.form_id = "alumno"
        self.helper.form_method = "post"
        self.fields['alumno'].queryset = alumnos
