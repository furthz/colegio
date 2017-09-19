from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelForm

from profiles.models import Profile
from register.models import Alumno, Apoderado, Personal, Promotor, Director, Cajero, Tesorero, Proveedor, Colegio
from utils.forms import ValidProfileFormMixin
from utils.models import TipoDocumento, TipoSexo, Departamento, Provincia, Distrito


class PersonaForm(ModelForm):

    direccion = forms.CharField(widget=forms.TextInput(attrs={'tabindex': '13', 'class': 'form-control'}), label="Direccion")
    referencia = forms.CharField(widget=forms.TextInput(attrs={'tabindex': '14', 'class': 'form-control'}), label="Referencia")
    departamento = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Departamento")
    provincia = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Provincia")
    distrito = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Distrito")
    tipo_cel = forms.ChoiceField(widget=forms.Select(attrs={'tabindex': '15', 'class': 'form-control'}), label="Tipo Movil",
                                 required=False)
    celular = forms.CharField(widget=forms.NumberInput(attrs={'tabindex': '16', 'class': 'form-control'}), label="Celular",
                              required=False)
    celulares = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'tabindex': '17', 'class': 'form-control'}), label="Números",
                                          required=False)

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
                                                          widget=forms.Select(attrs={'tabindex': '5', 'class': 'form-control'}))
        self.fields['sexo'] = forms.ChoiceField(choices=self.ChoiceTipoSexo,
                                                widget=forms.Select(attrs={'tabindex': '7', 'class': 'form-control'}))
        self.fields['departamento'] = forms.ChoiceField(choices = self.ChoiceDepartamento,
                                                        widget=forms.Select(attrs={'tabindex': '10', 'class': 'form-control'}))
        self.fields['provincia']= forms.ChoiceField(choices = self.ChoiceProvincia,
                                                    widget=forms.Select(attrs={'tabindex': '11', 'class': 'form-control'}))
        self.fields['distrito'] = forms.ChoiceField(choices = self.ChoiceDistrito,
                                                    widget=forms.Select(attrs={'tabindex': '12', 'class': 'form-control'}))
        self.fields['nombre'].widget.attrs = {'tabindex': '1', 'class': 'form-control'}
        self.fields['segundo_nombre'].widget.attrs = {'tabindex': '2', 'class': 'form-control'}
        self.fields['apellido_pa'].widget.attrs = {'tabindex': '3', 'class': 'form-control'}
        self.fields['apellido_ma'].widget.attrs = {'tabindex': '4', 'class': 'form-control'}
        self.fields['numero_documento'].widget.attrs = {'tabindex': '6', 'class': 'form-control'}
        self.fields['correo'].widget.attrs = {'tabindex': '9', 'class': 'form-control'}
        self.fields['fecha_nac'].widget.attrs = {'tabindex': '8', 'class': 'form-control'}

    class Meta:
        model = Profile
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class AlumnoForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Alumno", required=False)

    class Meta:
        model = Alumno
        fields = ['user', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class ApoderadoForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Apoderado", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parentesco'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Apoderado
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'parentesco', 'tipo_documento',
                  'numero_documento', 'sexo', 'correo', 'fecha_nac']


class PersonalForm(ValidProfileFormMixin, PersonaForm):

    class Meta:
        model = Personal
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class PromotorForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Promotor", required=False)

    class Meta:
        model = Promotor
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class DirectorForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Director", required=False)

    class Meta:
        model = Director
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class CajeroForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Cajero", required=False)

    class Meta:
        model = Cajero
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class TesoreroForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Tesorero", required=False)

    class Meta:
        model = Tesorero
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


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


class ColegioForm(ModelForm):

    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Direccion")
    referencia = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Referencia")
    departamento = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Departamento")
    provincia = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Provincia")
    distrito = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Distrito")
    tipo_cel = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Tipo Movil",
                                 required=False)
    celular = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Celular",
                              required=False)
    celulares = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}), label="Números",
                                          required=False)

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

    class Meta:
        model = Colegio
        fields = [
            'nombre',
            'ruc',
            'ugel',
            'departamento',
            'provincia',
            'distrito',
            'referencia',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['ruc'].widget.attrs.update({'class': 'form-control'})
        self.fields['ugel'].widget.attrs.update({'class': 'form-control'})
        self.fields['departamento'] = forms.ChoiceField(choices=self.ChoiceDepartamento,
                                                        widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['provincia'] = forms.ChoiceField(choices=self.ChoiceProvincia,
                                                     widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['distrito'] = forms.ChoiceField(choices=self.ChoiceDistrito,
                                                    widget=forms.Select(attrs={'class': 'form-control'}))


