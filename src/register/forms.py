from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from profiles.models import Profile
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm, SelectDateWidget

from register.models import Alumno, Apoderado, Personal, Promotor, Director, Cajero, Tesorero, Telefono, Proveedor
from utils.forms import ValidProfileFormMixin
from utils.models import TipoDocumento, TipoSexo, Departamento, Provincia, Distrito


class PersonaForm(ModelForm):

    direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Direccion")
    referencia = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Referencia")
    departamento = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label="Departamento")
    provincia = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Provincia")
    distrito = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Distrito")
    tipo_cel = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Tipo Movil", required=False)
    celular = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Celular", required=False)
    celulares = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}), label="Números", required=False)

    @property
    def ChoiceTipoDocumento(self):
        choices = [(tipo.id_tipo, tipo.descripcion) for tipo in TipoDocumento.objects.all()]
        return choices

    @property
    def ChoiceTipoSexo(self):
        choices = [(sex.id_sexo, sex.descripcion) for sex in TipoSexo.objects.all()]
        return choices

    @property
    def ChoiceDepartamento(self):
        choices = [(d.id_departamento, d.descripcion) for d in Departamento.objects.all()]
        return choices

    @property
    def ChoiceProvincia(self):
        choices = [(p.id_provincia, p.descripcion) for p in Provincia.objects.all()]
        return choices

    @property
    def ChoiceDistrito(self):
        choices = [(d.id_distrito, d.descripcion) for d in Distrito.objects.all()]
        return choices

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_documento'] = forms.ChoiceField(choices=self.ChoiceTipoDocumento,
                                                          widget=forms.Select(attrs={'class':'form-control'}))
        self.fields['sexo'] = forms.ChoiceField(choices=self.ChoiceTipoSexo,
                                                widget=forms.Select(attrs={'class':'form-control'}))
        self.fields['departamento'] = forms.ChoiceField(choices = self.ChoiceDepartamento,
                                                        widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['provincia']= forms.ChoiceField(choices = self.ChoiceProvincia,
                                                    widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['distrito'] = forms.ChoiceField(choices = self.ChoiceDistrito,
                                                    widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['nombre'].widget.attrs.update({'class':'form-control'})
        self.fields['segundo_nombre'].widget.attrs.update({'class':'form-control'})
        self.fields['apellido_pa'].widget.attrs.update({'class':'form-control'})
        self.fields['apellido_ma'].widget.attrs.update({'class':'form-control'})
        self.fields['numero_documento'].widget.attrs.update({'class':'form-control'})
        self.fields['correo'].widget.attrs.update({'class':'form-control'})
        self.fields['fecha_nac'].widget.attrs.update({'class': 'form-control'})


    class Meta:
        model = Profile
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class AlumnoForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Alumno", required=False)

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

    title = forms.CharField(label="Registrar Apoderado", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parentesco'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Apoderado
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'parentesco', 'tipo_documento',
                  'numero_documento', 'sexo', 'correo', 'fecha_nac']
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


class PersonalForm(ValidProfileFormMixin, PersonaForm):

    class Meta:
        model = Personal
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


class PromotorForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Promotor", required=False)

    class Meta:
        model = Promotor
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
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


class DirectorForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Director", required=False)

    class Meta:
        model = Director
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


class CajeroForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Cajero", required=False)

    class Meta:
        model = Cajero
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


class TesoreroForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Tesorero", required=False)

    class Meta:
        model = Tesorero
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


class ProveedorForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "idproveedor"
        self.helper.form_method = "post"

        self.helper.add_input(Submit('submit', 'Crear', css_class="btn btn-primary btn-block btn-flat"))

    class Meta:
        model = Proveedor
        fields = ['razon_social', 'ruc']
        labels = {
            'ruc': _('RUC'),
            'razon_social': _('Razón Social'),
        }
